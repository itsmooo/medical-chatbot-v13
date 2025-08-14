import { Document } from 'mongoose';
export type UserDocument = User & Document;
export declare enum UserRole {
    USER = "user",
    ADMIN = "admin",
    DOCTOR = "doctor"
}
export declare enum Gender {
    MALE = "male",
    FEMALE = "female",
    OTHER = "other"
}
export declare class User {
    name: string;
    email: string;
    password: string;
    role: UserRole;
    profileImage?: string;
    gender?: Gender;
    age?: number;
    phoneNumber?: string;
    address?: string;
    city?: string;
    country?: string;
    isEmailVerified: boolean;
    isPhoneVerified: boolean;
    lastLoginAt?: Date;
    isActive: boolean;
    createdAt: Date;
    updatedAt: Date;
}
export declare const UserSchema: import("mongoose").Schema<User, import("mongoose").Model<User, any, any, any, Document<unknown, any, User, any, {}> & User & {
    _id: import("mongoose").Types.ObjectId;
} & {
    __v: number;
}, any>, {}, {}, {}, {}, import("mongoose").DefaultSchemaOptions, User, Document<unknown, {}, import("mongoose").FlatRecord<User>, {}, import("mongoose").ResolveSchemaOptions<import("mongoose").DefaultSchemaOptions>> & import("mongoose").FlatRecord<User> & {
    _id: import("mongoose").Types.ObjectId;
} & {
    __v: number;
}>;
