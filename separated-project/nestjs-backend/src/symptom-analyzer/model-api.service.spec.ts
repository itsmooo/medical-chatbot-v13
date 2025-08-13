import { Test, TestingModule } from '@nestjs/testing';
import { ModelApiService } from './model-api.service';

describe('ModelApiService', () => {
  let service: ModelApiService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [ModelApiService],
    }).compile();

    service = module.get<ModelApiService>(ModelApiService);
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });
});