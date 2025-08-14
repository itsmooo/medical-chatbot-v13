import { ModelApiService } from './model-api.service';
export declare class SymptomAnalyzerController {
    private readonly modelApiService;
    constructor(modelApiService: ModelApiService);
    predictDisease(data: {
        symptoms: string[];
    }, req: any): Promise<any>;
    getUserPredictions(req: any): Promise<(import("mongoose").Document<unknown, {}, import("./entities/prediction.entity").PredictionDocument, {}, {}> & import("./entities/prediction.entity").Prediction & import("mongoose").Document<unknown, any, any, Record<string, any>, {}> & Required<{
        _id: unknown;
    }> & {
        __v: number;
    })[]>;
    getPredictionById(id: string, req: any): Promise<(import("mongoose").Document<unknown, {}, import("./entities/prediction.entity").PredictionDocument, {}, {}> & import("./entities/prediction.entity").Prediction & import("mongoose").Document<unknown, any, any, Record<string, any>, {}> & Required<{
        _id: unknown;
    }> & {
        __v: number;
    }) | {
        error: string;
    }>;
    getPredictionPdf(id: string, req: any, res: any): Promise<any>;
    getAllPredictions(): Promise<(import("mongoose").Document<unknown, {}, import("./entities/prediction.entity").PredictionDocument, {}, {}> & import("./entities/prediction.entity").Prediction & import("mongoose").Document<unknown, any, any, Record<string, any>, {}> & Required<{
        _id: unknown;
    }> & {
        __v: number;
    })[]>;
    checkHealth(): Promise<any>;
}
