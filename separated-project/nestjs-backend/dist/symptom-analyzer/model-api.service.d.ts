import { ConfigService } from '@nestjs/config';
import { Model } from 'mongoose';
import { Prediction, PredictionDocument } from './entities/prediction.entity';
import { Response } from 'express';
export declare class ModelApiService {
    private configService;
    private predictionModel;
    private readonly logger;
    private readonly apiUrl;
    constructor(configService: ConfigService, predictionModel: Model<PredictionDocument>);
    predictDisease(symptoms: string, userId?: string): Promise<any>;
    getUserPredictions(userId: string): Promise<(import("mongoose").Document<unknown, {}, PredictionDocument, {}, {}> & Prediction & import("mongoose").Document<unknown, any, any, Record<string, any>, {}> & Required<{
        _id: unknown;
    }> & {
        __v: number;
    })[]>;
    getPredictionById(id: string): Promise<(import("mongoose").Document<unknown, {}, PredictionDocument, {}, {}> & Prediction & import("mongoose").Document<unknown, any, any, Record<string, any>, {}> & Required<{
        _id: unknown;
    }> & {
        __v: number;
    }) | null>;
    getAllPredictions(): Promise<(import("mongoose").Document<unknown, {}, PredictionDocument, {}, {}> & Prediction & import("mongoose").Document<unknown, any, any, Record<string, any>, {}> & Required<{
        _id: unknown;
    }> & {
        __v: number;
    })[]>;
    generatePredictionPdf(prediction: PredictionDocument, res: Response): Promise<Response<any, Record<string, any>>>;
    checkHealth(): Promise<any>;
}
