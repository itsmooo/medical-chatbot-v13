import { Controller, Post, Body, Get } from '@nestjs/common';
import { ModelApiService } from './model-api.service';

@Controller('symptom-analyzer')
export class SymptomAnalyzerController {
  constructor(private readonly modelApiService: ModelApiService) {}

  @Post('predict')
  async predictDisease(@Body() data: { symptoms: string[] }) {
    // Join the symptoms array into a string since the model expects a string
    const symptomsText = Array.isArray(data.symptoms) 
      ? data.symptoms.join(', ')
      : data.symptoms;
    
    return await this.modelApiService.predictDisease(symptomsText);
  }

  @Get('health')
  async checkHealth() {
    return await this.modelApiService.checkHealth();
  }
}