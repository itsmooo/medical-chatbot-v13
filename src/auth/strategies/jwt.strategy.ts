import { Injectable } from '@nestjs/common';
import { PassportStrategy } from '@nestjs/passport';
import { ExtractJwt, Strategy } from 'passport-jwt';
import { ConfigService } from '@nestjs/config';

@Injectable()
export class JwtStrategy extends PassportStrategy(Strategy) {
  constructor(private configService: ConfigService) {
    super({
      jwtFromRequest: ExtractJwt.fromAuthHeaderAsBearerToken(),
      ignoreExpiration: false,
      secretOrKey: configService.get<string>('JWT_SECRET') || 'super-secret-key-change-in-production',
    });
  }

  async validate(payload: any) {
    console.log('JWT Strategy - Received payload:', payload);
    
    // Make sure name is included in the returned user object
    const user = { 
      userId: payload.sub, 
      email: payload.email,
      name: payload.name || '',
      role: payload.role
    };
    
    console.log('JWT Strategy - Returning user:', user);
    return user;
  }
}
