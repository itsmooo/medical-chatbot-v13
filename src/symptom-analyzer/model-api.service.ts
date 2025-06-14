import { Injectable, Logger, HttpException, HttpStatus } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import fetch from 'node-fetch';

@Injectable()
export class ModelApiService {
  private readonly logger = new Logger(ModelApiService.name);
  private readonly apiUrl: string;

  constructor(private configService: ConfigService) {
    this.apiUrl = this.configService.get<string>('MODEL_API_URL') || 'http://localhost:5000';
    this.logger.log(`Model API URL: ${this.apiUrl}`);
  }

  async predictDisease(symptoms: string) {
    try {
      const response = await fetch(`${this.apiUrl}/predict`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ symptoms }),
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`API returned ${response.status}: ${errorText}`);
      }

      return await response.json();
    } catch (error) {
      this.logger.error(`Error calling model API: ${error.message}`);
      throw new HttpException(
        'Failed to analyze symptoms',
        HttpStatus.INTERNAL_SERVER_ERROR,
      );
    }
  }

  async checkHealth() {
    try {
      const response = await fetch(`${this.apiUrl}/health`);
      return await response.json();
    } catch (error) {
      this.logger.error(`Health check failed: ${error.message}`);
      return { status: 'error', message: error.message };
    }
  }
}