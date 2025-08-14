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
Object.defineProperty(exports, "__esModule", { value: true });
exports.SymptomAnalyzerController = void 0;
const common_1 = require("@nestjs/common");
const jwt_auth_guard_1 = require("../auth/guards/jwt-auth.guard");
const roles_decorator_1 = require("../auth/decorators/roles.decorator");
const roles_guard_1 = require("../auth/guards/roles.guard");
const user_entity_1 = require("../auth/entities/user.entity");
const model_api_service_1 = require("./model-api.service");
let SymptomAnalyzerController = class SymptomAnalyzerController {
    modelApiService;
    constructor(modelApiService) {
        this.modelApiService = modelApiService;
    }
    async predictDisease(data, req) {
        const symptomsText = Array.isArray(data.symptoms)
            ? data.symptoms.join(', ')
            : data.symptoms;
        const userId = req.user.userId;
        return await this.modelApiService.predictDisease(symptomsText, userId);
    }
    async getUserPredictions(req) {
        const userId = req.user.userId;
        return await this.modelApiService.getUserPredictions(userId);
    }
    async getPredictionById(id, req) {
        const userId = req.user.userId;
        const prediction = await this.modelApiService.getPredictionById(id);
        if (prediction && (prediction.userId === userId || req.user.role === user_entity_1.UserRole.ADMIN)) {
            return prediction;
        }
        return { error: 'Prediction not found or access denied' };
    }
    async getPredictionPdf(id, req, res) {
        const userId = req.user.userId;
        const prediction = await this.modelApiService.getPredictionById(id);
        if (prediction && (prediction.userId === userId || req.user.role === user_entity_1.UserRole.ADMIN)) {
            return this.modelApiService.generatePredictionPdf(prediction, res);
        }
        return res.status(404).json({ error: 'Prediction not found or access denied' });
    }
    async getAllPredictions() {
        return await this.modelApiService.getAllPredictions();
    }
    async checkHealth() {
        return await this.modelApiService.checkHealth();
    }
};
exports.SymptomAnalyzerController = SymptomAnalyzerController;
__decorate([
    (0, common_1.Post)('predict'),
    (0, common_1.UseGuards)(jwt_auth_guard_1.JwtAuthGuard),
    __param(0, (0, common_1.Body)()),
    __param(1, (0, common_1.Req)()),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", [Object, Object]),
    __metadata("design:returntype", Promise)
], SymptomAnalyzerController.prototype, "predictDisease", null);
__decorate([
    (0, common_1.Get)('predictions'),
    (0, common_1.UseGuards)(jwt_auth_guard_1.JwtAuthGuard),
    __param(0, (0, common_1.Req)()),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", [Object]),
    __metadata("design:returntype", Promise)
], SymptomAnalyzerController.prototype, "getUserPredictions", null);
__decorate([
    (0, common_1.Get)('predictions/:id'),
    (0, common_1.UseGuards)(jwt_auth_guard_1.JwtAuthGuard),
    __param(0, (0, common_1.Param)('id')),
    __param(1, (0, common_1.Req)()),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", [String, Object]),
    __metadata("design:returntype", Promise)
], SymptomAnalyzerController.prototype, "getPredictionById", null);
__decorate([
    (0, common_1.Get)('predictions/:id/pdf'),
    (0, common_1.UseGuards)(jwt_auth_guard_1.JwtAuthGuard),
    __param(0, (0, common_1.Param)('id')),
    __param(1, (0, common_1.Req)()),
    __param(2, (0, common_1.Res)()),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", [String, Object, Object]),
    __metadata("design:returntype", Promise)
], SymptomAnalyzerController.prototype, "getPredictionPdf", null);
__decorate([
    (0, common_1.Get)('admin/predictions'),
    (0, common_1.UseGuards)(jwt_auth_guard_1.JwtAuthGuard, roles_guard_1.RolesGuard),
    (0, roles_decorator_1.Roles)(user_entity_1.UserRole.ADMIN),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", []),
    __metadata("design:returntype", Promise)
], SymptomAnalyzerController.prototype, "getAllPredictions", null);
__decorate([
    (0, common_1.Get)('health'),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", []),
    __metadata("design:returntype", Promise)
], SymptomAnalyzerController.prototype, "checkHealth", null);
exports.SymptomAnalyzerController = SymptomAnalyzerController = __decorate([
    (0, common_1.Controller)('symptom-analyzer'),
    __metadata("design:paramtypes", [model_api_service_1.ModelApiService])
], SymptomAnalyzerController);
//# sourceMappingURL=symptom-analyzer.controller.js.map