import { Prop, Schema, SchemaFactory } from '@nestjs/mongoose';
import { Document } from 'mongoose';

export type UserDocument = User & Document;

export enum UserRole {
  USER = 'user',
  ADMIN = 'admin',
  DOCTOR = 'doctor',
}

export enum Gender {
  MALE = 'male',
  FEMALE = 'female',
  OTHER = 'other',
}

@Schema({ 
  timestamps: true,
  collection: 'users'
})
export class User {
  @Prop({ 
    required: true, 
    trim: true,
    minlength: 2,
    maxlength: 50
  })
  name: string;

  @Prop({ 
    required: true, 
    unique: true,
    lowercase: true,
    trim: true,
    match: /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  })
  email: string;

  @Prop({ 
    required: true,
    minlength: 6
  })
  password: string;

  @Prop({ 
    enum: UserRole, 
    default: UserRole.USER,
    index: true
  })
  role: UserRole;

  @Prop({ 
    trim: true,
    maxlength: 200
  })
  profileImage?: string;

  @Prop({ 
    enum: Gender,
    required: false
  })
  gender?: Gender;

  @Prop({ 
    min: 0,
    max: 150
  })
  age?: number;

  @Prop({ 
    trim: true,
    maxlength: 100
  })
  phoneNumber?: string;

  @Prop({ 
    trim: true,
    maxlength: 200
  })
  address?: string;

  @Prop({ 
    trim: true,
    maxlength: 100
  })
  city?: string;

  @Prop({ 
    trim: true,
    maxlength: 100
  })
  country?: string;

  @Prop({ 
    default: false
  })
  isEmailVerified: boolean;

  @Prop({ 
    default: false
  })
  isPhoneVerified: boolean;

  @Prop()
  lastLoginAt?: Date;

  @Prop({ 
    default: true
  })
  isActive: boolean;

  @Prop()
  createdAt: Date;

  @Prop()
  updatedAt: Date;
}

export const UserSchema = SchemaFactory.createForClass(User);

// Add indexes for better query performance
UserSchema.index({ email: 1 });
UserSchema.index({ role: 1 });
UserSchema.index({ createdAt: -1 });
UserSchema.index({ isActive: 1 });
