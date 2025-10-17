import pg, { Client } from "pg";
import dotenv from "dotenv";
dotenv.config();

const { Pool } = pg;

export const pool = new Pool({
  user: process.env.PGUSER,
  password: process.env.PGPASSWORD,
  host: process.env.PGHOST,
  port: process.env.PGPORT,
  database: process.env.PGDATABASE,
});

// ---------------------------
//  🔹 INSERIR MEDIÇÃO
// ---------------------------
export async function createMeasurement(data,horario,subarea_observacao_id,ph,temperatura,turbidez) {
  const client = await pool.client();
  
  try {
    await client.query("BEGIN");

    const insertMediaQuery = `
      INSERT INTO medicacao (data,horario,subarea_observacao_id)
      VALUES ($1,$2,$3)
      RETURNING ID;
    `;

    const medicaoSend = await client.query(insertMediaQuery, [data,horario,subarea_observacao_id]);
    const medicaoId = medicaoSend.rows[0].id;

    const insertValueOriginal = `
      INSERT INTO valores_medidos_original (medicao_id,ph,temperatura,turbidez)
      VALUES ($1,$2,$3,$4)
      RETURNING *;
    `;

    const medicaoValueOriginalSend = await client.query(insertValueOriginal, [medicaoId,ph,temperatura,turbidez]);

    // Valores simulados
    const ph_convertido = ph * 0.1;
    const turbidez_convertido = turbidez * 0.2;
    const temperatura_convertido = temperatura * 0.3;

    const insertValueConverted = `
      INSERT INTO valores_medidos_convertido (medicao_id, ph, temperatura,turbidez)
      VALUES ($1,$2,$3,$4)
      RETURNING *;
    `;

    const medicaoValueConvertedSend = await client.query(insertValueConverted, [medicaoId,ph_convertido,temperatura_convertido,turbidez_convertido]);

    await client.query("COMMIT");

    return {
      medicaoId,
      valor: medicaoValueOriginalSend.rows[0],
      valor_convertido: medicaoValueConvertedSend.rows[0],
    }

  } catch (error) {
    console.error("Error: ", error);
    throw error;
  }
}











/*
// ---------------------------
//  🔹 CONSULTAR TODAS AS ÁREAS
// ---------------------------
export async function getAllObservationAreas() {
  try {
    const query = `
      SELECT id, nome, descricao, local, id_area_pai
      FROM areas_de_observacao
      ORDER BY id ASC;
    `;
    const result = await pool.query(query);
    return result.rows;
  } catch (error) {
    console.error("Erro ao buscar áreas de observação:", error);
    throw error;
  }
}

// ---------------------------
//  🔹 CONSULTAR SUBÁREAS POR ÁREA
// ---------------------------
export async function getSubareasByArea(areaId) {
  try {
    const query = `
      SELECT id, nome, descricao, local, area_de_observacao_id
      FROM subareas_de_observacao
      WHERE area_de_observacao_id = $1
      ORDER BY id ASC;
    `;
    const result = await pool.query(query, [areaId]);
    return result.rows;
  } catch (error) {
    console.error("Erro ao buscar subáreas:", error);
    throw error;
  }
}

// ---------------------------
//  🔹 CONSULTAR MEDIÇÕES POR SUBÁREA
// ---------------------------
export async function getMeasurementsBySubarea(subareaId) {
  try {
    const query = `
      SELECT 
        m.id AS medicacao_id,
        m.data,
        m.horario,
        vo.ph AS ph_original,
        vo.temperatura AS temperatura_original,
        vo.turbidez AS turbidez_original,
        vc.ph AS ph_convertido,
        vc.temperatura AS temperatura_convertida,
        vc.turbidez AS turbidez_convertida
      FROM medicacao m
      JOIN valores_medidos_original vo ON m.id = vo.medicacao_id
      JOIN valores_medidos_convertido vc ON m.id = vc.medicacao_id
      WHERE m.subarea_observacao_id = $1
      ORDER BY m.data DESC, m.horario DESC;
    `;
    const result = await pool.query(query, [subareaId]);
    return result.rows;
  } catch (error) {
    console.error("Erro ao buscar medições da subárea:", error);
    throw error;
  }
}
