import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';
import { ModelApiService } from './model-api.service';
import { SymptomAnalyzerController } from './symptom-analyzer.controller';

@Module({
  imports: [ConfigModule],
  controllers: [SymptomAnalyzerController],
  providers: [ModelApiService],
  exports: [ModelApiService],
})
export class SymptomAnalyzerModule {}