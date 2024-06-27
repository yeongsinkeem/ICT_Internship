import { Inject, Injectable, InternalServerErrorException, NotFoundException } from '@nestjs/common';
import { IncomeDist } from "src/entities/income-dist.entity";
import { IsNull, Not, Repository } from 'typeorm';

@Injectable()
export class IncomeDistService {
  constructor(
    @Inject("INCOME_DIST_PROVIDERS")
    private incomeDistRepository: Repository<IncomeDist>,
  ) {}

  async find(sido_name: string, sigungu_name: string, emd_name?: string) {
    try {
      // 기본 조건 설정
      const baseDistrict: any = {
        sido_name: sido_name,
      };
  
      if (emd_name) {
        // Query로 읍면동을 받은 경우
        const entity = await this.incomeDistRepository.findOne({
          where: { ...baseDistrict, sigungu_name: sigungu_name, emd_name: emd_name },
          select: ['month_avg_income', 'total']
        });
  
        if (!entity) 
          throw new NotFoundException(`소득 정보가 존재하지 않습니다.`);
  
        // 해당 시군구 내의 모든 읍면동을 조회하여 정렬
        const allEntities = await this.incomeDistRepository.find({
          where: { ...baseDistrict, sigungu_name: sigungu_name, emd_name: Not("") },
          order: { month_avg_income: 'DESC' },
          select: ['month_avg_income', 'total', 'emd_name']
        });

        // 순위 계산
        const rank = allEntities.findIndex(e => e.emd_name === emd_name) + 1;
  
        return {
          status: 200,
          message: "소득 정보 조회 성공",
          data: {
            rank,
            total_records: allEntities.length,
            entity,
          }
        };
      } 
      else {
        // Query로 시군구까지만 받은 경우
        const entity = await this.incomeDistRepository.findOne({
          where: { ... baseDistrict, sigungu_name: sigungu_name, emd_name: ""},
          order: { month_avg_income : 'DESC' },
          select: [ 'month_avg_income', 'total' ]
        });

        if (!entity)
          throw new NotFoundException(`소득 정보가 존재하지 않습니다.`);

        // 해당 시도 내의 모든 시군구를 조회하여 정렬
        const allEntities = await this.incomeDistRepository.find({
          where: { ...baseDistrict, emd_name: "" },
          order: { month_avg_income: 'DESC' },
          select: ['month_avg_income', 'total', 'sigungu_name']
        });
        
        // 순위 계산
        const rank = allEntities.findIndex(e => e.sigungu_name === sigungu_name) + 1;
  
        return {
          status: 200,
          message: '소득 정보 조회 성공',
          data: {
            rank,
            total_records: allEntities.length,
            entity,
          }
        };
      }
    } catch (error) {
      console.error('소득 정보 조회 중 오류 발생:', error);
      throw new InternalServerErrorException(`소득 정보 조회 중 오류 발생 - ${error.message}`);
    }
  }

  async findGeo(sido_name: string, sigungu_name: string, emd_name?: string){
    try {
      // 기본 조건 설정
      const baseDistrict: any = {
        sido_name: sido_name,
      };

      // Query로 읍면동까지 받은 경우 
      if (emd_name) {
        const entity = await this.incomeDistRepository.findOne({
          where: { ...baseDistrict, sigungu_name: sigungu_name, emd_name: emd_name },
          select: ['coordinate']
        });

        if ( !entity  || entity.coordinate === "" )
          throw new NotFoundException(`좌표 정보가 존재하지 않습니다.`);

        return {
          status: 200,
          message: "좌표 정보 조회 성공",
          data: {
            entity
          }
        };
      }
      else {
        // Query로 시군구까지만 받은 경우
        const entity = await this.incomeDistRepository.findOne({
          where: { ...baseDistrict, sigungu_name: sigungu_name, emd_name: "" },
          select: ['coordinate']
        });

        if ( !entity || entity.coordinate === "" )
          throw new NotFoundException(`좌표 정보가 존재하지 않습니다.`);

        return {
          status: 200,
          message: "좌표 정보 조회 성공",
          data: {
            entity
          }
        };
      }
    }
    catch (error) {
      console.error('소득 정보 조회 중 오류 발생:', error);
      throw new InternalServerErrorException(`소득 정보 조회 중 오류 발생 - ${error.message}`);
}  
}
}

  

