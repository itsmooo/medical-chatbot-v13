import { Injectable, UnauthorizedException, ConflictException } from '@nestjs/common';
import { JwtService } from '@nestjs/jwt';
import { InjectModel } from '@nestjs/mongoose';
import { Model, Types } from 'mongoose';
import * as bcrypt from 'bcrypt';
import { User, UserDocument, UserRole } from './entities/user.entity';
import { CreateUserDto } from './dto/create-user.dto';
import { SignInDto } from './dto/sign-in.dto';

@Injectable()
export class AuthService {
  constructor(
    @InjectModel(User.name)
    private userModel: Model<UserDocument>,
    private jwtService: JwtService,
  ) {}

  async signUp(createUserDto: CreateUserDto): Promise<{ id: string; name: string; email: string; role: UserRole }> {
    // Check if user already exists
    const existingUser = await this.userModel.findOne({ email: createUserDto.email }).exec();

    if (existingUser) {
      throw new ConflictException('User with this email already exists');
    }

    // Hash password
    const hashedPassword = await bcrypt.hash(createUserDto.password, 10);

    // Create new user
    const newUser = new this.userModel({
      name: createUserDto.name,
      email: createUserDto.email,
      password: hashedPassword,
      role: UserRole.PATIENT, // Default role is patient
    });

    const savedUser = await newUser.save();

    // Return user without password
    const result = {
      id: (savedUser._id as Types.ObjectId).toString(),
      name: savedUser.name,
      email: savedUser.email,
      role: savedUser.role as UserRole
    };
    return result;
  }

  async signIn(signInDto: SignInDto): Promise<{ token: string; user: { id: string; name: string; email: string; role: UserRole } }> {
    const user = await this.userModel.findOne({ email: signInDto.email }).exec();

    if (!user) {
      throw new UnauthorizedException('Invalid credentials');
    }

    // Verify password
    const isPasswordValid = await bcrypt.compare(signInDto.password, user.password);

    if (!isPasswordValid) {
      throw new UnauthorizedException('Invalid credentials');
    }

    // Debug logs to see what's in the user object
    console.log('User from database:', {
      id: user._id,
      name: user.name,
      email: user.email,
      role: user.role
    });

    // Ensure we have a valid name
    const userName = user.name || '';
    console.log('User name from database:', userName);
    
    // Generate JWT token with explicit name field
    const payload = { 
      sub: (user._id as Types.ObjectId).toString(), 
      email: user.email, 
      name: userName, // Ensure name is included and never undefined
      role: user.role 
    };
    console.log('JWT payload:', payload);
    const token = this.jwtService.sign(payload);

    // Return token and user info without password
    const userInfo = {
      id: (user._id as Types.ObjectId).toString(),
      name: user.name,
      email: user.email,
      role: user.role as UserRole
    };
    
    return {
      token,
      user: userInfo,
    };
  }

  async validateUser(email: string, password: string): Promise<any> {
    const user = await this.userModel.findOne({ email }).exec();

    if (user && await bcrypt.compare(password, user.password)) {
      const result = {
        id: (user._id as Types.ObjectId).toString(),
        name: user.name,
        email: user.email,
        role: user.role as UserRole
      };
      return result;
    }
    
    return null;
  }

  async createAdminUser(adminDto: CreateUserDto): Promise<UserDocument> {
    // Check if user already exists
    const existingUser = await this.userModel.findOne({ email: adminDto.email }).exec();

    if (existingUser) {
      throw new ConflictException('User with this email already exists');
    }

    // Hash password
    const hashedPassword = await bcrypt.hash(adminDto.password, 10);

    // Create admin user
    const adminUser = new this.userModel({
      name: adminDto.name,
      email: adminDto.email,
      password: hashedPassword,
      role: UserRole.ADMIN,
    });

    return adminUser.save();
  }
}
