import { Module } from '@nestjs/common';
import { ChatController } from './chat.controller';
import { ChatService } from './chat.service';
import { SymptomAnalyzerModule } from '../symptom-analyzer/symptom-analyzer.module';

@Module({
  imports: [SymptomAnalyzerModule],
  controllers: [ChatController],
  providers: [ChatService],
})
export class ChatModule {}