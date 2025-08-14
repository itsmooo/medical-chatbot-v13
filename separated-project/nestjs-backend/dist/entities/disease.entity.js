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
Object.defineProperty(exports, "__esModule", { value: true });
exports.DiseaseSchema = exports.Disease = exports.DiseaseSeverity = exports.DiseaseCategory = void 0;
const mongoose_1 = require("@nestjs/mongoose");
var DiseaseCategory;
(function (DiseaseCategory) {
    DiseaseCategory["INFECTIOUS"] = "infectious";
    DiseaseCategory["CARDIOVASCULAR"] = "cardiovascular";
    DiseaseCategory["RESPIRATORY"] = "respiratory";
    DiseaseCategory["NEUROLOGICAL"] = "neurological";
    DiseaseCategory["ENDOCRINE"] = "endocrine";
    DiseaseCategory["GASTROINTESTINAL"] = "gastrointestinal";
    DiseaseCategory["MUSCULOSKELETAL"] = "musculoskeletal";
    DiseaseCategory["DERMATOLOGICAL"] = "dermatological";
    DiseaseCategory["PSYCHIATRIC"] = "psychiatric";
    DiseaseCategory["ONCOLOGICAL"] = "oncological";
    DiseaseCategory["OTHER"] = "other";
})(DiseaseCategory || (exports.DiseaseCategory = DiseaseCategory = {}));
var DiseaseSeverity;
(function (DiseaseSeverity) {
    DiseaseSeverity["MILD"] = "mild";
    DiseaseSeverity["MODERATE"] = "moderate";
    DiseaseSeverity["SEVERE"] = "severe";
    DiseaseSeverity["CRITICAL"] = "critical";
})(DiseaseSeverity || (exports.DiseaseSeverity = DiseaseSeverity = {}));
let Disease = class Disease {
    name;
    description;
    category;
    severity;
    symptoms;
    precautions;
    treatments;
    riskFactors;
    complications;
    diagnosticTests;
    specialists;
    tags;
    statistics;
    metadata;
    createdAt;
    updatedAt;
};
exports.Disease = Disease;
__decorate([
    (0, mongoose_1.Prop)({
        required: true,
        unique: true,
        trim: true,
        maxlength: 100
    }),
    __metadata("design:type", String)
], Disease.prototype, "name", void 0);
__decorate([
    (0, mongoose_1.Prop)({
        required: true,
        trim: true,
        maxlength: 1000
    }),
    __metadata("design:type", String)
], Disease.prototype, "description", void 0);
__decorate([
    (0, mongoose_1.Prop)({
        type: String,
        enum: Object.values(DiseaseCategory),
        required: true,
        index: true
    }),
    __metadata("design:type", String)
], Disease.prototype, "category", void 0);
__decorate([
    (0, mongoose_1.Prop)({
        type: String,
        enum: Object.values(DiseaseSeverity),
        required: true,
        index: true
    }),
    __metadata("design:type", String)
], Disease.prototype, "severity", void 0);
__decorate([
    (0, mongoose_1.Prop)({
        type: [Object],
        required: true,
        validate: {
            validator: function (symptoms) {
                return symptoms.length > 0 && symptoms.length <= 50;
            },
            message: 'Disease must have between 1 and 50 symptoms'
        }
    }),
    __metadata("design:type", Array)
], Disease.prototype, "symptoms", void 0);
__decorate([
    (0, mongoose_1.Prop)({
        type: [Object],
        required: true,
        validate: {
            validator: function (precautions) {
                return precautions.length > 0 && precautions.length <= 20;
            },
            message: 'Disease must have between 1 and 20 precautions'
        }
    }),
    __metadata("design:type", Array)
], Disease.prototype, "precautions", void 0);
__decorate([
    (0, mongoose_1.Prop)({
        type: [Object],
        default: []
    }),
    __metadata("design:type", Array)
], Disease.prototype, "treatments", void 0);
__decorate([
    (0, mongoose_1.Prop)({
        type: [String],
        default: []
    }),
    __metadata("design:type", Array)
], Disease.prototype, "riskFactors", void 0);
__decorate([
    (0, mongoose_1.Prop)({
        type: [String],
        default: []
    }),
    __metadata("design:type", Array)
], Disease.prototype, "complications", void 0);
__decorate([
    (0, mongoose_1.Prop)({
        type: [String],
        default: []
    }),
    __metadata("design:type", Array)
], Disease.prototype, "diagnosticTests", void 0);
__decorate([
    (0, mongoose_1.Prop)({
        type: [String],
        default: []
    }),
    __metadata("design:type", Array)
], Disease.prototype, "specialists", void 0);
__decorate([
    (0, mongoose_1.Prop)({
        type: [String],
        default: []
    }),
    __metadata("design:type", Array)
], Disease.prototype, "tags", void 0);
__decorate([
    (0, mongoose_1.Prop)({
        type: Object,
        default: {}
    }),
    __metadata("design:type", Object)
], Disease.prototype, "statistics", void 0);
__decorate([
    (0, mongoose_1.Prop)({
        type: Object,
        default: {}
    }),
    __metadata("design:type", Object)
], Disease.prototype, "metadata", void 0);
__decorate([
    (0, mongoose_1.Prop)(),
    __metadata("design:type", Date)
], Disease.prototype, "createdAt", void 0);
__decorate([
    (0, mongoose_1.Prop)(),
    __metadata("design:type", Date)
], Disease.prototype, "updatedAt", void 0);
exports.Disease = Disease = __decorate([
    (0, mongoose_1.Schema)({
        timestamps: true,
        collection: 'diseases'
    })
], Disease);
exports.DiseaseSchema = mongoose_1.SchemaFactory.createForClass(Disease);
exports.DiseaseSchema.index({ name: 1 });
exports.DiseaseSchema.index({ category: 1, severity: 1 });
exports.DiseaseSchema.index({ 'symptoms.name': 1 });
exports.DiseaseSchema.index({ tags: 1 });
exports.DiseaseSchema.index({ createdAt: -1 });
exports.DiseaseSchema.index({ 'statistics.prevalence': -1 });
//# sourceMappingURL=disease.entity.js.map