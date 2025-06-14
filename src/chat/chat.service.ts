import { Injectable, Logger } from '@nestjs/common';
import { ModelApiService } from '../symptom-analyzer/model-api.service';

@Injectable()
export class ChatService {
  private readonly logger = new Logger(ChatService.name);
  private chatHistory: Record<string, any[]> = {};

  constructor(private readonly modelApiService: ModelApiService) {}

  async processMessage(message: string, userId: string = 'anonymous') {
    try {
      // Store user message in history
      this.addMessageToHistory(userId, 'user', message);

      // Analyze symptoms using the model API
      const analysis = await this.modelApiService.predictDisease(message);

      // Store bot response in history
      this.addMessageToHistory(
        userId,
        'bot',
        analysis.response,
        analysis.diseases,
      );

      return analysis;
    } catch (error) {
      this.logger.error(`Error processing message: ${error.message}`);

      const fallbackResponse =
        "I'm sorry, I couldn't analyze your symptoms properly. Could you provide more details about how you're feeling?";

      // Store error response in history
      this.addMessageToHistory(userId, 'bot', fallbackResponse);

      return {
        response: fallbackResponse,
        diseases: [],
        error: error.message,
      };
    }
  }

  getChatHistory(userId: string = 'anonymous') {
    return this.chatHistory[userId] || [];
  }

  private addMessageToHistory(
    userId: string,
    sender: 'user' | 'bot',
    content: string,
    diseases: any[] = [],
  ) {
    if (!this.chatHistory[userId]) {
      this.chatHistory[userId] = [];
    }

    this.chatHistory[userId].push({
      id: Date.now().toString(),
      sender,
      content,
      timestamp: new Date(),
      ...(sender === 'bot' && diseases.length > 0 ? { diseases } : {}),
    });

    // Limit history size
    if (this.chatHistory[userId].length > 100) {
      this.chatHistory[userId] = this.chatHistory[userId].slice(-100);
    }
  }
}
