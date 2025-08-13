import { 
  Controller, 
  Post, 
  Body, 
  HttpCode, 
  HttpStatus, 
  UseGuards, 
  Get, 
  Request, 
  UseInterceptors, 
  UploadedFile, 
  Param, 
  Res,
  BadRequestException,
  NotFoundException
} from '@nestjs/common';
import { FileInterceptor } from '@nestjs/platform-express';
import { Response } from 'express';
import { diskStorage } from 'multer';
import { extname, join } from 'path';
import { existsSync } from 'fs';
import { AuthService } from './auth.service';
import { CreateUserDto } from './dto/create-user.dto';
import { SignInDto } from './dto/sign-in.dto';
import { JwtAuthGuard } from './guards/jwt-auth.guard';
import { RolesGuard } from './guards/roles.guard';
import { Roles } from './decorators/roles.decorator';
import { UserRole } from './entities/user.entity';

// Multer configuration for profile images
const profileImageStorage = diskStorage({
  destination: './uploads/profile-images',
  filename: (req, file, callback) => {
    // Extract user ID from request (set by JWT guard)
    const userId = (req as any).user?.userId || 'unknown';
    const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
    const extension = extname(file.originalname);
    callback(null, `profile-${userId}-${uniqueSuffix}${extension}`);
  },
});

const imageFileFilter = (req: any, file: any, callback: any) => {
  if (!file.originalname.match(/\.(jpg|jpeg|png|gif)$/)) {
    return callback(new BadRequestException('Only image files are allowed!'), false);
  }
  callback(null, true);
};

@Controller('auth')
export class AuthController {
  constructor(private readonly authService: AuthService) {}

  @Post('signup')
  async signUp(@Body() createUserDto: CreateUserDto) {
    const user = await this.authService.signUp(createUserDto);
    return {
      message: 'User registered successfully',
      user,
    };
  }

  @HttpCode(HttpStatus.OK)
  @Post('signin')
  async signIn(@Body() signInDto: SignInDto) {
    return this.authService.signIn(signInDto);
  }

  @UseGuards(JwtAuthGuard)
  @Get('profile')
  getProfile(@Request() req) {
    return req.user;
  }

  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles(UserRole.ADMIN)
  @Post('admin/create')
  async createAdmin(@Body() createUserDto: CreateUserDto) {
    const admin = await this.authService.createAdminUser(createUserDto);
    return {
      message: 'Admin user created successfully',
      admin,
    };
  }

  @UseGuards(JwtAuthGuard)
  @Post('upload-profile-image')
  @UseInterceptors(
    FileInterceptor('profileImage', {
      storage: profileImageStorage,
      fileFilter: imageFileFilter,
      limits: {
        fileSize: 5 * 1024 * 1024, // 5MB limit
      },
    }),
  )
  async uploadProfileImage(
    @UploadedFile() file: Express.Multer.File,
    @Request() req,
  ) {
    if (!file) {
      throw new BadRequestException('No file uploaded');
    }

    const userId = req.user.userId;
    
    // Save file path to user profile in database
    await this.authService.updateUserProfileImage(userId, file.filename);

    return {
      message: 'Profile image uploaded successfully',
      filename: file.filename,
      path: `/uploads/profile-images/${file.filename}`,
    };
  }

  @Get('profile-image/:userId')
  async getProfileImage(@Param('userId') userId: string, @Res() res: Response) {
    try {
      // Get user's profile image filename from database
      const user = await this.authService.findUserById(userId);
      
      if (!user || !user.profileImage) {
        throw new NotFoundException('Profile image not found');
      }

      const imagePath = join(process.cwd(), 'uploads', 'profile-images', user.profileImage);
      
      if (!existsSync(imagePath)) {
        throw new NotFoundException('Image file not found');
      }

      // Set appropriate content type
      const extension = extname(user.profileImage).toLowerCase();
      const mimeTypes = {
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.gif': 'image/gif',
      };
      
      const contentType = mimeTypes[extension] || 'application/octet-stream';
      res.setHeader('Content-Type', contentType);
      
      return res.sendFile(imagePath);
    } catch (error) {
      throw new NotFoundException('Profile image not found');
    }
  }
}
