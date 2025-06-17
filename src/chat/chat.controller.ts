import { Controller, Post, Body, Get, Query, UseGuards, Req } from '@nestjs/common';
import { JwtAuthGuard } from '../auth/guards/jwt-auth.guard';
import { Roles } from '../auth/decorators/roles.decorator';
import { RolesGuard } from '../auth/guards/roles.guard';
import { UserRole } from '../auth/entities/user.entity';
import { ChatService } from './chat.service';
import { ChatMessageDto } from './dto/chat-message.dto';

@Controller('chat')
export class ChatController {
  constructor(private readonly chatService: ChatService) {}

  @Post('message')
  @UseGuards(JwtAuthGuard)
  async processMessage(@Body() chatMessageDto: ChatMessageDto, @Req() req) {
    // Get user ID from authenticated request
    const userId = req.user.userId;
    return this.chatService.processMessage(chatMessageDto.message, userId);
  }

  @Get('history')
  @UseGuards(JwtAuthGuard)
  async getChatHistory(@Req() req) {
    const userId = req.user.userId;
    return this.chatService.getChatHistory(userId);
  }

  @Get('admin/history')
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles(UserRole.ADMIN)
  async getAllChatHistory(@Query('userId') userId: string) {
    // If userId is provided, get history for that user, otherwise return all
    if (userId) {
      return this.chatService.getChatHistory(userId);
    }
    return this.chatService.getAllChatHistory();
  }
}