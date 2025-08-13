import { Module } from '@nestjs/common';
import { MongooseModule } from '@nestjs/mongoose';
import { ChatController } from './chat.controller';
import { ChatService } from './chat.service';
import { SymptomAnalyzerModule } from '../symptom-analyzer/symptom-analyzer.module';
import { ChatMessage, ChatMessageSchema } from './entities/chat-message.entity';

@Module({
  imports: [
    MongooseModule.forFeature([{ name: ChatMessage.name, schema: ChatMessageSchema }]),
    SymptomAnalyzerModule
  ],
  controllers: [ChatController],
  providers: [ChatService],
})
export class ChatModule {}