"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const testing_1 = require("@nestjs/testing");
const chat_controller_1 = require("./chat.controller");
describe('ChatController', () => {
    let controller;
    beforeEach(async () => {
        const module = await testing_1.Test.createTestingModule({
            controllers: [chat_controller_1.ChatController],
        }).compile();
        controller = module.get(chat_controller_1.ChatController);
    });
    it('should be defined', () => {
        expect(controller).toBeDefined();
    });
});
//# sourceMappingURL=chat.controller.spec.js.map