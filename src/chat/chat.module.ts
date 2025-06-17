import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { ChatController } from './chat.controller';
import { ChatService } from './chat.service';
import { SymptomAnalyzerModule } from '../symptom-analyzer/symptom-analyzer.module';
import { ChatMessage } from './entities/chat-message.entity';

@Module({
  imports: [
    TypeOrmModule.forFeature([ChatMessage]),
    SymptomAnalyzerModule
  ],
  controllers: [ChatController],
  providers: [ChatService],
})
export class ChatModule {}