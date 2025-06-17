import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';
import { MongooseModule } from '@nestjs/mongoose';
import { SymptomAnalyzerController } from './symptom-analyzer.controller';
import { ModelApiService } from './model-api.service';
import { Prediction, PredictionSchema } from './entities/prediction.entity';

@Module({
  imports: [
    ConfigModule,
    MongooseModule.forFeature([{ name: Prediction.name, schema: PredictionSchema }])
  ],
  controllers: [SymptomAnalyzerController],
  providers: [ModelApiService],
  exports: [ModelApiService],
})
export class SymptomAnalyzerModule {}