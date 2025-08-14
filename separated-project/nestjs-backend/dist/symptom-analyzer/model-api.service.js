"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
var __param = (this && this.__param) || function (paramIndex, decorator) {
    return function (target, key) { decorator(target, key, paramIndex); }
};
var ModelApiService_1;
Object.defineProperty(exports, "__esModule", { value: true });
exports.ModelApiService = void 0;
const common_1 = require("@nestjs/common");
const config_1 = require("@nestjs/config");
const mongoose_1 = require("@nestjs/mongoose");
const mongoose_2 = require("mongoose");
const node_fetch_1 = require("node-fetch");
const prediction_entity_1 = require("./entities/prediction.entity");
const PDFDocument = require("pdfkit");
let ModelApiService = ModelApiService_1 = class ModelApiService {
    configService;
    predictionModel;
    logger = new common_1.Logger(ModelApiService_1.name);
    apiUrl;
    constructor(configService, predictionModel) {
        this.configService = configService;
        this.predictionModel = predictionModel;
        this.apiUrl = this.configService.get('MODEL_API_URL') || 'http://localhost:5000';
        this.logger.log(`Model API URL: ${this.apiUrl}`);
    }
    async predictDisease(symptoms, userId) {
        try {
            const response = await (0, node_fetch_1.default)(`${this.apiUrl}/predict`, {
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
            if (userId) {
                const prediction = new this.predictionModel({
                    symptoms,
                    diseases: result.diseases || [],
                    response: result.response,
                    userId: new mongoose_2.Types.ObjectId(userId)
                });
                await prediction.save();
            }
            return result;
        }
        catch (error) {
            this.logger.error(`Error calling model API: ${error.message}`);
            throw new common_1.HttpException('Failed to analyze symptoms', common_1.HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }
    async getUserPredictions(userId) {
        return this.predictionModel.find({ userId: new mongoose_2.Types.ObjectId(userId) })
            .sort({ createdAt: -1 })
            .exec();
    }
    async getPredictionById(id) {
        return this.predictionModel.findById(id).exec();
    }
    async getAllPredictions() {
        return this.predictionModel.find()
            .sort({ createdAt: -1 })
            .exec();
    }
    async generatePredictionPdf(prediction, res) {
        const doc = new PDFDocument();
        res.setHeader('Content-Type', 'application/pdf');
        const predictionId = prediction._id instanceof mongoose_2.Types.ObjectId ? prediction._id.toString() : String(prediction._id);
        res.setHeader('Content-Disposition', `attachment; filename=prediction-${predictionId}.pdf`);
        doc.pipe(res);
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
        doc.end();
        return res;
    }
    async checkHealth() {
        try {
            const response = await (0, node_fetch_1.default)(`${this.apiUrl}/health`);
            return await response.json();
        }
        catch (error) {
            this.logger.error(`Health check failed: ${error.message}`);
            return { status: 'error', message: error.message };
        }
    }
};
exports.ModelApiService = ModelApiService;
exports.ModelApiService = ModelApiService = ModelApiService_1 = __decorate([
    (0, common_1.Injectable)(),
    __param(1, (0, mongoose_1.InjectModel)(prediction_entity_1.Prediction.name)),
    __metadata("design:paramtypes", [config_1.ConfigService,
        mongoose_2.Model])
], ModelApiService);
//# sourceMappingURL=model-api.service.js.map