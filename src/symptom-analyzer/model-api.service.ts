import { Injectable, Logger, HttpException, HttpStatus } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { InjectModel } from '@nestjs/mongoose';
import { Model, Types } from 'mongoose';
import fetch from 'node-fetch';
import { Prediction, PredictionDocument } from './entities/prediction.entity';
import * as PDFDocument from 'pdfkit';
import { Response } from 'express';

@Injectable()
export class ModelApiService {
  private readonly logger = new Logger(ModelApiService.name);
  private readonly apiUrl: string;

  constructor(
    private configService: ConfigService,
    @InjectModel(Prediction.name)
    private predictionModel: Model<PredictionDocument>,
  ) {
    this.apiUrl = this.configService.get<string>('MODEL_API_URL') || 'http://localhost:5000';
    this.logger.log(`Model API URL: ${this.apiUrl}`);
  }

  async predictDisease(symptoms: string, userId?: string) {
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

      const result = await response.json();
      
      // Save prediction if userId is provided
      if (userId) {
        const prediction = new this.predictionModel({
          symptoms,
          diseases: result.diseases || [],
          response: result.response,
          userId: new Types.ObjectId(userId)
        });
        await prediction.save();
      }
      
      return result;
    } catch (error) {
      this.logger.error(`Error calling model API: ${error.message}`);
      throw new HttpException(
        'Failed to analyze symptoms',
        HttpStatus.INTERNAL_SERVER_ERROR,
      );
    }
  }

  async getUserPredictions(userId: string) {
    return this.predictionModel.find({ userId: new Types.ObjectId(userId) })
      .sort({ createdAt: -1 })
      .exec();
  }

  async getPredictionById(id: string) {
    return this.predictionModel.findById(id).exec();
  }
  
  async getAllPredictions() {
    return this.predictionModel.find()
      .sort({ createdAt: -1 })
      .exec();
  }
  
  async generatePredictionPdf(prediction: PredictionDocument, res: Response) {
    const doc = new PDFDocument();
    
    // Set response headers for PDF download
    res.setHeader('Content-Type', 'application/pdf');
    const predictionId = prediction._id instanceof Types.ObjectId ? prediction._id.toString() : String(prediction._id);
    res.setHeader('Content-Disposition', `attachment; filename=prediction-${predictionId}.pdf`);
    
    // Pipe the PDF document to the response
    doc.pipe(res);
    
    // Add content to PDF
    doc.fontSize(25).text('Disease Prediction Report', { align: 'center' });
    doc.moveDown();
    doc.fontSize(14).text(`Date: ${prediction.createdAt.toLocaleDateString()}`, { align: 'right' });
    doc.moveDown();
    
    doc.fontSize(16).text('Patient Symptoms:', { underline: true });
    doc.fontSize(12).text(prediction.symptoms);
    doc.moveDown();
    
    doc.fontSize(16).text('Analysis Results:', { underline: true });
    doc.fontSize(12).text(prediction.response);
    doc.moveDown();
    
    if (prediction.diseases && prediction.diseases.length > 0) {
      doc.fontSize(16).text('Possible Diseases:', { underline: true });
      prediction.diseases.forEach((disease, index) => {
        doc.fontSize(12).text(`${index + 1}. ${disease.name} - Confidence: ${disease.confidence}%`);
      });
    }
    
    // Finalize the PDF and end the stream
    doc.end();
    
    return res;
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