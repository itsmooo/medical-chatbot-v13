"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.SymptomAnalyzerModule = void 0;
const common_1 = require("@nestjs/common");
const config_1 = require("@nestjs/config");
const mongoose_1 = require("@nestjs/mongoose");
const symptom_analyzer_controller_1 = require("./symptom-analyzer.controller");
const model_api_service_1 = require("./model-api.service");
const prediction_entity_1 = require("./entities/prediction.entity");
let SymptomAnalyzerModule = class SymptomAnalyzerModule {
};
exports.SymptomAnalyzerModule = SymptomAnalyzerModule;
exports.SymptomAnalyzerModule = SymptomAnalyzerModule = __decorate([
    (0, common_1.Module)({
        imports: [
            config_1.ConfigModule,
            mongoose_1.MongooseModule.forFeature([{ name: prediction_entity_1.Prediction.name, schema: prediction_entity_1.PredictionSchema }])
        ],
        controllers: [symptom_analyzer_controller_1.SymptomAnalyzerController],
        providers: [model_api_service_1.ModelApiService],
        exports: [model_api_service_1.ModelApiService],
    })
], SymptomAnalyzerModule);
//# sourceMappingURL=symptom-analyzer.module.js.map