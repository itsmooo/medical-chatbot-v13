import { Response } from 'express';
import { AuthService } from './auth.service';
import { CreateUserDto } from './dto/create-user.dto';
import { SignInDto } from './dto/sign-in.dto';
import { UserRole } from './entities/user.entity';
export declare class AuthController {
    private readonly authService;
    constructor(authService: AuthService);
    signUp(createUserDto: CreateUserDto): Promise<{
        message: string;
        user: {
            id: string;
            name: string;
            email: string;
            role: UserRole;
        };
    }>;
    signIn(signInDto: SignInDto): Promise<{
        token: string;
        user: {
            id: string;
            name: string;
            email: string;
            role: UserRole;
        };
    }>;
    getProfile(req: any): any;
    createAdmin(createUserDto: CreateUserDto): Promise<{
        message: string;
        admin: import("./entities/user.entity").UserDocument;
    }>;
    uploadProfileImage(file: Express.Multer.File, req: any): Promise<{
        message: string;
        filename: string;
        path: string;
    }>;
    getProfileImage(userId: string, res: Response): Promise<void>;
}
