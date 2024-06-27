import { Test, TestingModule } from '@nestjs/testing';
import { IncomeDistService } from './income-dist.service';

describe('IncomeDistService', () => {
  let service: IncomeDistService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [IncomeDistService],
    }).compile();

    service = module.get<IncomeDistService>(IncomeDistService);
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });
});
