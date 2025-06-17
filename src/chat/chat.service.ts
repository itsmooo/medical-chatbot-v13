import { Injectable, Logger } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { ModelApiService } from '../symptom-analyzer/model-api.service';
import { ChatMessage, MessageSender } from './entities/chat-message.entity';

@Injectable()
export class ChatService {
  private readonly logger = new Logger(ChatService.name);

  constructor(
    private readonly modelApiService: ModelApiService,
    @InjectRepository(ChatMessage)
    private chatMessageRepository: Repository<ChatMessage>
  ) {}

  async processMessage(message: string, userId: string = 'anonymous') {
    try {
      // Store user message in database
      await this.addMessageToHistory(userId, MessageSender.USER, message);

      // Analyze symptoms using the model API
      const analysis = await this.modelApiService.predictDisease(message, userId);

      // Store bot response in database
      await this.addMessageToHistory(
        userId,
        MessageSender.BOT,
        analysis.response,
        analysis.diseases,
      );

      return analysis;
    } catch (error) {
      this.logger.error(`Error processing message: ${error.message}`);

      const fallbackResponse =
        "I'm sorry, I couldn't analyze your symptoms properly. Could you provide more details about how you're feeling?";

      // Store error response in database
      await this.addMessageToHistory(userId, MessageSender.BOT, fallbackResponse);

      return {
        response: fallbackResponse,
        diseases: [],
        error: error.message,
      };
    }
  }

  async getChatHistory(userId: string = 'anonymous') {
    return this.chatMessageRepository.find({
      where: { userId },
      order: { timestamp: 'ASC' }
    });
  }
  
  async getAllChatHistory() {
    return this.chatMessageRepository.find({
      order: { timestamp: 'ASC' },
      relations: ['user']
    });
  }

  private async addMessageToHistory(
    userId: string,
    sender: MessageSender,
    content: string,
    diseases: any[] = [],
  ) {
    // Create new chat message entity
    const chatMessage = this.chatMessageRepository.create({
      sender,
      content,
      userId,
      diseases: sender === MessageSender.BOT && diseases.length > 0 ? diseases : [],
    });

    // Save to database
    return this.chatMessageRepository.save(chatMessage);
  }
}
