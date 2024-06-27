import { IncomeDist } from "src/entities/income-dist.entity";
import { DataSource } from "typeorm";


export const incomeDistProviders = [
    {
        provide: "INCOME_DIST_PROVIDERS",
        useFactory: (dataSource: DataSource) => dataSource.getRepository(IncomeDist),
        inject: ["DATA_SOURCE"],
    },
];