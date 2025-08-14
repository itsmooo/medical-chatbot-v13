import { JwtService } from '@nestjs/jwt';
import { Model } from 'mongoose';
import { UserDocument, UserRole } from './entities/user.entity';
import { CreateUserDto } from './dto/create-user.dto';
import { SignInDto } from './dto/sign-in.dto';
export declare class AuthService {
    private userModel;
    private jwtService;
    constructor(userModel: Model<UserDocument>, jwtService: JwtService);
    signUp(createUserDto: CreateUserDto): Promise<{
        id: string;
        name: string;
        email: string;
        role: UserRole;
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
    validateUser(email: string, password: string): Promise<any>;
    createAdminUser(adminDto: CreateUserDto): Promise<UserDocument>;
    findUserById(userId: string): Promise<UserDocument>;
    updateUserProfileImage(userId: string, profileImageFilename: string): Promise<UserDocument>;
}
