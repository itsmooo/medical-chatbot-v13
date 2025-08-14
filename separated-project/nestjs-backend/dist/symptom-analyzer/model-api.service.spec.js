"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const testing_1 = require("@nestjs/testing");
const model_api_service_1 = require("./model-api.service");
describe('ModelApiService', () => {
    let service;
    beforeEach(async () => {
        const module = await testing_1.Test.createTestingModule({
            providers: [model_api_service_1.ModelApiService],
        }).compile();
        service = module.get(model_api_service_1.ModelApiService);
    });
    it('should be defined', () => {
        expect(service).toBeDefined();
    });
});
//# sourceMappingURL=model-api.service.spec.js.map