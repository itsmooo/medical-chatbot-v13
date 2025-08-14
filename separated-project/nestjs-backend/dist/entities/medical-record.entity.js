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
exports.MedicalRecordSchema = exports.MedicalRecord = exports.BloodType = exports.RecordStatus = exports.RecordType = void 0;
const mongoose_1 = require("@nestjs/mongoose");
const mongoose_2 = require("mongoose");
var RecordType;
(function (RecordType) {
    RecordType["SYMPTOM_RECORD"] = "symptom_record";
    RecordType["DIAGNOSIS"] = "diagnosis";
    RecordType["TREATMENT"] = "treatment";
    RecordType["MEDICATION"] = "medication";
    RecordType["LAB_RESULT"] = "lab_result";
    RecordType["IMAGING"] = "imaging";
    RecordType["SURGERY"] = "surgery";
    RecordType["FOLLOW_UP"] = "follow_up";
    RecordType["EMERGENCY"] = "emergency";
})(RecordType || (exports.RecordType = RecordType = {}));
var RecordStatus;
(function (RecordStatus) {
    RecordStatus["ACTIVE"] = "active";
    RecordStatus["RESOLVED"] = "resolved";
    RecordStatus["ONGOING"] = "ongoing";
    RecordStatus["ARCHIVED"] = "archived";
})(RecordStatus || (exports.RecordStatus = RecordStatus = {}));
var BloodType;
(function (BloodType) {
    BloodType["A_POSITIVE"] = "A+";
    BloodType["A_NEGATIVE"] = "A-";
    BloodType["B_POSITIVE"] = "B+";
    BloodType["B_NEGATIVE"] = "B-";
    BloodType["AB_POSITIVE"] = "AB+";
    BloodType["AB_NEGATIVE"] = "AB-";
    BloodType["O_POSITIVE"] = "O+";
    BloodType["O_NEGATIVE"] = "O-";
})(BloodType || (exports.BloodType = BloodType = {}));
let MedicalRecord = class MedicalRecord {
    userId;
    recordType;
    status;
    title;
    description;
    date;
    vitalSigns;
    medications;
    labResults;
    surgeries;
    allergies;
    chronicConditions;
    familyHistory;
    lifestyleFactors;
    tags;
    attachments;
    doctorNotes;
    patientNotes;
    metadata;
    createdAt;
    updatedAt;
};
exports.MedicalRecord = MedicalRecord;
__decorate([
    (0, mongoose_1.Prop)({
        type: mongoose_2.Schema.Types.ObjectId,
        ref: 'User',
        required: true,
        index: true
    }),
    __metadata("design:type", mongoose_2.Types.ObjectId)
], MedicalRecord.prototype, "userId", void 0);
__decorate([
    (0, mongoose_1.Prop)({
        type: String,
        enum: Object.values(RecordType),
        required: true,
        index: true
    }),
    __metadata("design:type", String)
], MedicalRecord.prototype, "recordType", void 0);
__decorate([
    (0, mongoose_1.Prop)({
        type: String,
        enum: Object.values(RecordStatus),
        default: RecordStatus.ACTIVE,
        index: true
    }),
    __metadata("design:type", String)
], MedicalRecord.prototype, "status", void 0);
__decorate([
    (0, mongoose_1.Prop)({
        required: true,
        trim: true,
        maxlength: 500
    }),
    __metadata("design:type", String)
], MedicalRecord.prototype, "title", void 0);
__decorate([
    (0, mongoose_1.Prop)({
        required: true,
        trim: true,
        maxlength: 2000
    }),
    __metadata("design:type", String)
], MedicalRecord.prototype, "description", void 0);
__decorate([
    (0, mongoose_1.Prop)({
        type: Date,
        required: true
    }),
    __metadata("design:type", Date)
], MedicalRecord.prototype, "date", void 0);
__decorate([
    (0, mongoose_1.Prop)({
        type: Object,
        default: null
    }),
    __metadata("design:type", Object)
], MedicalRecord.prototype, "vitalSigns", void 0);
__decorate([
    (0, mongoose_1.Prop)({
        type: [Object],
        default: []
    }),
    __metadata("design:type", Array)
], MedicalRecord.prototype, "medications", void 0);
__decorate([
    (0, mongoose_1.Prop)({
        type: [Object],
        default: []
    }),
    __metadata("design:type", Array)
], MedicalRecord.prototype, "labResults", void 0);
__decorate([
    (0, mongoose_1.Prop)({
        type: [Object],
        default: []
    }),
    __metadata("design:type", Array)
], MedicalRecord.prototype, "surgeries", void 0);
__decorate([
    (0, mongoose_1.Prop)({
        type: [String],
        default: []
    }),
    __metadata("design:type", Array)
], MedicalRecord.prototype, "allergies", void 0);
__decorate([
    (0, mongoose_1.Prop)({
        type: [String],
        default: []
    }),
    __metadata("design:type", Array)
], MedicalRecord.prototype, "chronicConditions", void 0);
__decorate([
    (0, mongoose_1.Prop)({
        type: [String],
        default: []
    }),
    __metadata("design:type", Array)
], MedicalRecord.prototype, "familyHistory", void 0);
__decorate([
    (0, mongoose_1.Prop)({
        type: [String],
        default: []
    }),
    __metadata("design:type", Array)
], MedicalRecord.prototype, "lifestyleFactors", void 0);
__decorate([
    (0, mongoose_1.Prop)({
        type: [String],
        default: []
    }),
    __metadata("design:type", Array)
], MedicalRecord.prototype, "tags", void 0);
__decorate([
    (0, mongoose_1.Prop)({
        type: [String],
        default: []
    }),
    __metadata("design:type", Array)
], MedicalRecord.prototype, "attachments", void 0);
__decorate([
    (0, mongoose_1.Prop)({
        type: String,
        default: null
    }),
    __metadata("design:type", String)
], MedicalRecord.prototype, "doctorNotes", void 0);
__decorate([
    (0, mongoose_1.Prop)({
        type: String,
        default: null
    }),
    __metadata("design:type", String)
], MedicalRecord.prototype, "patientNotes", void 0);
__decorate([
    (0, mongoose_1.Prop)({
        type: Object,
        default: {}
    }),
    __metadata("design:type", Object)
], MedicalRecord.prototype, "metadata", void 0);
__decorate([
    (0, mongoose_1.Prop)(),
    __metadata("design:type", Date)
], MedicalRecord.prototype, "createdAt", void 0);
__decorate([
    (0, mongoose_1.Prop)(),
    __metadata("design:type", Date)
], MedicalRecord.prototype, "updatedAt", void 0);
exports.MedicalRecord = MedicalRecord = __decorate([
    (0, mongoose_1.Schema)({
        timestamps: true,
        collection: 'medical_records'
    })
], MedicalRecord);
exports.MedicalRecordSchema = mongoose_1.SchemaFactory.createForClass(MedicalRecord);
exports.MedicalRecordSchema.index({ userId: 1, date: -1 });
exports.MedicalRecordSchema.index({ userId: 1, recordType: 1 });
exports.MedicalRecordSchema.index({ userId: 1, status: 1 });
exports.MedicalRecordSchema.index({ recordType: 1, date: -1 });
exports.MedicalRecordSchema.index({ 'medications.name': 1 });
exports.MedicalRecordSchema.index({ 'labResults.testName': 1 });
exports.MedicalRecordSchema.index({ tags: 1 });
exports.MedicalRecordSchema.index({ createdAt: -1 });
//# sourceMappingURL=medical-record.entity.js.map