import { Controller, Post, Body, Get, Query } from '@nestjs/common';
import { ChatService } from './chat.service';
import { ChatMessageDto } from './dto/chat-message.dto';

@Controller('chat')
export class ChatController {
  constructor(private readonly chatService: ChatService) {}

  @Post('message')
  async processMessage(@Body() chatMessageDto: ChatMessageDto) {
    return this.chatService.processMessage(chatMessageDto.message, chatMessageDto.userId);
  }

  @Get('history')
  async getChatHistory(@Query('userId') userId: string) {
    return this.chatService.getChatHistory(userId);
  }
}