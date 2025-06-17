import { Controller, Post, Body, Get, UseGuards, Req, Param, Res } from '@nestjs/common';
import { JwtAuthGuard } from '../auth/guards/jwt-auth.guard';
import { Roles } from '../auth/decorators/roles.decorator';
import { RolesGuard } from '../auth/guards/roles.guard';
import { UserRole } from '../auth/entities/user.entity';
import { ModelApiService } from './model-api.service';

@Controller('symptom-analyzer')
export class SymptomAnalyzerController {
  constructor(private readonly modelApiService: ModelApiService) {}

  @Post('predict')
  @UseGuards(JwtAuthGuard)
  async predictDisease(@Body() data: { symptoms: string[] }, @Req() req) {
    // Join the symptoms array into a string since the model expects a string
    const symptomsText = Array.isArray(data.symptoms) 
      ? data.symptoms.join(', ')
      : data.symptoms;
    
    // Get user ID from the authenticated request
    const userId = req.user.userId;
    
    return await this.modelApiService.predictDisease(symptomsText, userId);
  }
  
  @Get('predictions')
  @UseGuards(JwtAuthGuard)
  async getUserPredictions(@Req() req) {
    const userId = req.user.userId;
    return await this.modelApiService.getUserPredictions(userId);
  }
  
  @Get('predictions/:id')
  @UseGuards(JwtAuthGuard)
  async getPredictionById(@Param('id') id: string, @Req() req) {
    const userId = req.user.userId;
    const prediction = await this.modelApiService.getPredictionById(id);
    
    // Check if prediction belongs to the user or user is admin
    if (prediction && (prediction.userId === userId || req.user.role === UserRole.ADMIN)) {
      return prediction;
    }
    
    return { error: 'Prediction not found or access denied' };
  }
  
  @Get('predictions/:id/pdf')
  @UseGuards(JwtAuthGuard)
  async getPredictionPdf(@Param('id') id: string, @Req() req, @Res() res) {
    const userId = req.user.userId;
    const prediction = await this.modelApiService.getPredictionById(id);
    
    // Check if prediction belongs to the user or user is admin
    if (prediction && (prediction.userId === userId || req.user.role === UserRole.ADMIN)) {
      // Generate PDF and send it as a response
      return this.modelApiService.generatePredictionPdf(prediction, res);
    }
    
    return res.status(404).json({ error: 'Prediction not found or access denied' });
  }
  
  @Get('admin/predictions')
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles(UserRole.ADMIN)
  async getAllPredictions() {
    return await this.modelApiService.getAllPredictions();
  }
  
  @Get('health')
  async checkHealth() {
    return await this.modelApiService.checkHealth();
  }
}