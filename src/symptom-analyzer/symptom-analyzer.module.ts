import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';
import { TypeOrmModule } from '@nestjs/typeorm';
import { SymptomAnalyzerController } from './symptom-analyzer.controller';
import { ModelApiService } from './model-api.service';
import { Prediction } from './entities/prediction.entity';

@Module({
  imports: [
    ConfigModule,
    TypeOrmModule.forFeature([Prediction])
  ],
  controllers: [SymptomAnalyzerController],
  providers: [ModelApiService],
  exports: [ModelApiService],
})
export class SymptomAnalyzerModule {}