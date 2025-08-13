import { Injectable, Logger } from '@nestjs/common';
import { InjectModel } from '@nestjs/mongoose';
import { Model, Types } from 'mongoose';
import { ModelApiService } from '../symptom-analyzer/model-api.service';
import { ChatMessage, ChatMessageDocument, MessageSender } from './entities/chat-message.entity';

@Injectable()
export class ChatService {
  private readonly logger = new Logger(ChatService.name);

  constructor(
    private readonly modelApiService: ModelApiService,
    @InjectModel(ChatMessage.name)
    private chatMessageModel: Model<ChatMessageDocument>
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
    return this.chatMessageModel.find({
      userId: userId !== 'anonymous' ? new Types.ObjectId(userId) : userId
    })
    .sort({ timestamp: 1 })
    .exec();
  }
  
  async getAllChatHistory() {
    return this.chatMessageModel.find()
      .sort({ timestamp: 1 })
      .populate('userId', 'name email') // Populate user fields we need
      .exec();
  }

  private async addMessageToHistory(
    userId: string,
    sender: MessageSender,
    content: string,
    diseases: any[] = [],
  ) {
    // Create new chat message document
    const chatMessage = new this.chatMessageModel({
      sender,
      content,
      userId: userId !== 'anonymous' ? new Types.ObjectId(userId) : userId,
      diseases: sender === MessageSender.BOT && diseases.length > 0 ? diseases : [],
    });

    // Save to database
    return chatMessage.save();
  }
}
