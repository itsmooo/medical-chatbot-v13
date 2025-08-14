"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
var __param = (this && this.__param) || function (paramIndex, decorator) {
    return function (target, key) { decorator(target, key, paramIndex); }
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.AuthService = void 0;
const common_1 = require("@nestjs/common");
const jwt_1 = require("@nestjs/jwt");
const mongoose_1 = require("@nestjs/mongoose");
const mongoose_2 = require("mongoose");
const bcrypt = require("bcrypt");
const user_entity_1 = require("./entities/user.entity");
let AuthService = class AuthService {
    userModel;
    jwtService;
    constructor(userModel, jwtService) {
        this.userModel = userModel;
        this.jwtService = jwtService;
    }
    async signUp(createUserDto) {
        const existingUser = await this.userModel.findOne({ email: createUserDto.email }).exec();
        if (existingUser) {
            throw new common_1.ConflictException('User with this email already exists');
        }
        const hashedPassword = await bcrypt.hash(createUserDto.password, 10);
        const newUser = new this.userModel({
            name: createUserDto.name,
            email: createUserDto.email,
            password: hashedPassword,
            role: user_entity_1.UserRole.USER,
        });
        const savedUser = await newUser.save();
        const result = {
            id: savedUser._id.toString(),
            name: savedUser.name,
            email: savedUser.email,
            role: savedUser.role
        };
        return result;
    }
    async signIn(signInDto) {
        const user = await this.userModel.findOne({ email: signInDto.email }).exec();
        if (!user) {
            throw new common_1.UnauthorizedException('Invalid credentials');
        }
        const isPasswordValid = await bcrypt.compare(signInDto.password, user.password);
        if (!isPasswordValid) {
            throw new common_1.UnauthorizedException('Invalid credentials');
        }
        console.log('User from database:', {
            id: user._id,
            name: user.name,
            email: user.email,
            role: user.role
        });
        const userName = user.name || '';
        console.log('User name from database:', userName);
        const payload = {
            sub: user._id.toString(),
            email: user.email,
            name: userName,
            role: user.role
        };
        console.log('JWT payload:', payload);
        const token = this.jwtService.sign(payload);
        const userInfo = {
            id: user._id.toString(),
            name: user.name,
            email: user.email,
            role: user.role
        };
        return {
            token,
            user: userInfo,
        };
    }
    async validateUser(email, password) {
        const user = await this.userModel.findOne({ email }).exec();
        if (user && await bcrypt.compare(password, user.password)) {
            const result = {
                id: user._id.toString(),
                name: user.name,
                email: user.email,
                role: user.role
            };
            return result;
        }
        return null;
    }
    async createAdminUser(adminDto) {
        const existingUser = await this.userModel.findOne({ email: adminDto.email }).exec();
        if (existingUser) {
            throw new common_1.ConflictException('User with this email already exists');
        }
        const hashedPassword = await bcrypt.hash(adminDto.password, 10);
        const adminUser = new this.userModel({
            name: adminDto.name,
            email: adminDto.email,
            password: hashedPassword,
            role: user_entity_1.UserRole.ADMIN,
        });
        return adminUser.save();
    }
    async findUserById(userId) {
        const user = await this.userModel.findById(userId).exec();
        if (!user) {
            throw new common_1.NotFoundException('User not found');
        }
        return user;
    }
    async updateUserProfileImage(userId, profileImageFilename) {
        const user = await this.userModel.findByIdAndUpdate(userId, { profileImage: profileImageFilename }, { new: true }).exec();
        if (!user) {
            throw new common_1.NotFoundException('User not found');
        }
        return user;
    }
};
exports.AuthService = AuthService;
exports.AuthService = AuthService = __decorate([
    (0, common_1.Injectable)(),
    __param(0, (0, mongoose_1.InjectModel)(user_entity_1.User.name)),
    __metadata("design:paramtypes", [mongoose_2.Model,
        jwt_1.JwtService])
], AuthService);
//# sourceMappingURL=auth.service.js.map