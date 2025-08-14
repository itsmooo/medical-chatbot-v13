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
exports.PredictionSchema = exports.Prediction = exports.PredictionAccuracy = exports.PredictionStatus = void 0;
const mongoose_1 = require("@nestjs/mongoose");
const mongoose_2 = require("mongoose");
var PredictionStatus;
(function (PredictionStatus) {
    PredictionStatus["PENDING"] = "pending";
    PredictionStatus["PROCESSING"] = "processing";
    PredictionStatus["COMPLETED"] = "completed";
    PredictionStatus["FAILED"] = "failed";
})(PredictionStatus || (exports.PredictionStatus = PredictionStatus = {}));
var PredictionAccuracy;
(function (PredictionAccuracy) {
    PredictionAccuracy["LOW"] = "low";
    PredictionAccuracy["MEDIUM"] = "medium";
    PredictionAccuracy["HIGH"] = "high";
})(PredictionAccuracy || (exports.PredictionAccuracy = PredictionAccuracy = {}));
let Prediction = class Prediction {
    symptoms;
    diseases;
    response;
    userId;
    status;
    accuracy;
    symptomAnalysis;
    modelPerformance;
    tags;
    isFollowUpRequired;
    followUpDate;
    followUpNotes;
    metadata;
    createdAt;
    updatedAt;
};
exports.Prediction = Prediction;
__decorate([
    (0, mongoose_1.Prop)({
        required: true,
        trim: true,
        maxlength: 1000
    }),
    __metadata("design:type", String)
], Prediction.prototype, "symptoms", void 0);
__decorate([
    (0, mongoose_1.Prop)({
        type: [Object],
        default: [],
        validate: {
            validator: function (diseases) {
                return diseases.length <= 20;
            },
            message: 'Cannot have more than 20 diseases per prediction'
        }
    }),
    __metadata("design:type", Array)
], Prediction.prototype, "diseases", void 0);
__decorate([
    (0, mongoose_1.Prop)({
        required: true,
        trim: true,
        maxlength: 2000
    }),
    __metadata("design:type", String)
], Prediction.prototype, "response", void 0);
__decorate([
    (0, mongoose_1.Prop)({
        type: mongoose_2.Schema.Types.ObjectId,
        ref: 'User',
        required: true,
        index: true
    }),
    __metadata("design:type", mongoose_2.Types.ObjectId)
], Prediction.prototype, "userId", void 0);
__decorate([
    (0, mongoose_1.Prop)({
        type: String,
        enum: Object.values(PredictionStatus),
        default: PredictionStatus.PENDING,
        index: true
    }),
    __metadata("design:type", String)
], Prediction.prototype, "status", void 0);
__decorate([
    (0, mongoose_1.Prop)({
        type: String,
        enum: Object.values(PredictionAccuracy),
        default: PredictionAccuracy.MEDIUM
    }),
    __metadata("design:type", String)
], Prediction.prototype, "accuracy", void 0);
__decorate([
    (0, mongoose_1.Prop)({
        type: Object,
        default: null
    }),
    __metadata("design:type", Object)
], Prediction.prototype, "symptomAnalysis", void 0);
__decorate([
    (0, mongoose_1.Prop)({
        type: Object,
        default: null
    }),
    __metadata("design:type", Object)
], Prediction.prototype, "modelPerformance", void 0);
__decorate([
    (0, mongoose_1.Prop)({
        type: [String],
        default: []
    }),
    __metadata("design:type", Array)
], Prediction.prototype, "tags", void 0);
__decorate([
    (0, mongoose_1.Prop)({
        default: false
    }),
    __metadata("design:type", Boolean)
], Prediction.prototype, "isFollowUpRequired", void 0);
__decorate([
    (0, mongoose_1.Prop)({
        type: Date,
        default: null
    }),
    __metadata("design:type", Date)
], Prediction.prototype, "followUpDate", void 0);
__decorate([
    (0, mongoose_1.Prop)({
        type: String,
        default: null
    }),
    __metadata("design:type", String)
], Prediction.prototype, "followUpNotes", void 0);
__decorate([
    (0, mongoose_1.Prop)({
        type: Object,
        default: {}
    }),
    __metadata("design:type", Object)
], Prediction.prototype, "metadata", void 0);
__decorate([
    (0, mongoose_1.Prop)(),
    __metadata("design:type", Date)
], Prediction.prototype, "createdAt", void 0);
__decorate([
    (0, mongoose_1.Prop)(),
    __metadata("design:type", Date)
], Prediction.prototype, "updatedAt", void 0);
exports.Prediction = Prediction = __decorate([
    (0, mongoose_1.Schema)({
        timestamps: true,
        collection: 'predictions'
    })
], Prediction);
exports.PredictionSchema = mongoose_1.SchemaFactory.createForClass(Prediction);
exports.PredictionSchema.index({ userId: 1, createdAt: -1 });
exports.PredictionSchema.index({ status: 1, createdAt: -1 });
exports.PredictionSchema.index({ accuracy: 1, createdAt: -1 });
exports.PredictionSchema.index({ isFollowUpRequired: 1, followUpDate: 1 });
exports.PredictionSchema.index({ tags: 1 });
exports.PredictionSchema.index({ 'diseases.disease': 1 });
exports.PredictionSchema.index({ 'diseases.severity': 1 });
exports.PredictionSchema.index({ 'diseases.urgency': 1 });
//# sourceMappingURL=prediction.entity.js.map