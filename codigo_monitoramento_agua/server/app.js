import express from "express";
import bodyParser from "body-parser";
import {
  createMeasurement,
  // getAllObservationAreas,
  // getSubareasByArea,
  // getMeasurementsBySubarea
} from "./bd.js";

const app = express();
const port = 3000;

app.use(bodyParser.json());

app.user((req,res, next) => {
  const agora = new Date().toDateString();
  console.log(`[${agora}] ${req.method} ${req.url} - IP: ${req.ip}`);
  next();
});

// =======================
// 🔹 ROTA PRINCIPAL
// =======================
app.get("/", (req,res) => {
  res.send("Api do sistema rodando!");
});

// =======================
// 🔹 CRIAR MEDIÇÃO
// =======================
app.post('/medicao', (req,res) => {
  console.log("POST /medicao recebida: ", req.body);

  const { data, horario, subareaId, ph, temperatura, turbidez} = req.body;

  if (!data || !horario || !subareaId || ph === undefined || temperatura === undefined || turbidez === undefined) {
    return res.status(400).json({ error: "Dados incompletos!" });
  }

  try {
    const resultado = createMeasurement(data,horario,subareaId,ph,temperatura,turbidez);
    res.status(201).json({ sucesso: true, mensagem: "Dados adicionados corretamente!", dados: resultado });
  } catch (error) {
    console.error("Erro ao lançar medição: ", error);
    res.status(500).json({ error: "error ao lançar a medição" });
    throw error;
  }

});










app.post("/medicao", async (req, res) => {
  console.log("POST /medicao recebida:", req.body);

  const { data, horario, subareaId, ph, temperatura, turbidez } = req.body;

  if (!data || !horario || !subareaId || ph === undefined || temperatura === undefined || turbidez === undefined) {
    return res.status(400).json({ error: "Dados incompletos!" });
  }

  try {
    const resultado = await createMeasurement(data, horario, subareaId, ph, temperatura, turbidez);
    res.status(201).json({ sucesso: true, message: "Medição registrada com sucesso", dados: resultado });
  } catch (error) {
    console.error("Erro ao criar medição:", error);
    res.status(500).json({ sucesso: false, erro: error.message });
  }
});





/*



// =======================
// 🔹 LISTAR TODAS AS ÁREAS
// =======================
app.get("/areas", async (req, res) => {
  try {
    const areas = await getAllObservationAreas();
    res.status(200).json(areas);
  } catch (error) {
    console.error("Erro ao buscar áreas:", error);
    res.status(500).json({ erro: "Erro ao buscar áreas" });
  }
});

// =======================
// 🔹 LISTAR SUBÁREAS DE UMA ÁREA
// =======================
app.get("/areas/:id/subareas", async (req, res) => {
  const areaId = req.params.id;
  try {
    const subareas = await getSubareasByArea(areaId);
    if (subareas.length === 0) {
      return res.status(404).json({ message: "Nenhuma subárea encontrada para esta área." });
    }
    res.status(200).json(subareas);
  } catch (error) {
    console.error("Erro ao buscar subáreas:", error);
    res.status(500).json({ erro: "Erro ao buscar subáreas" });
  }
});

// =======================
// 🔹 LISTAR MEDIÇÕES DE UMA SUBÁREA
// =======================
app.get("/subareas/:id/medicoes", async (req, res) => {
  const subareaId = req.params.id;
  try {
    const medicoes = await getMeasurementsBySubarea(subareaId);
    if (medicoes.length === 0) {
      return res.status(404).json({ message: "Nenhuma medição encontrada para esta subárea." });
    }
    res.status(200).json(medicoes);
  } catch (error) {
    console.error("Erro ao buscar medições:", error);
    res.status(500).json({ erro: "Erro ao buscar medições" });
  }
});

// =======================
// 🔹 INICIALIZAÇÃO DO SERVIDOR
// =======================
app.listen(port, () => {
  console.log(`🌍 Servidor rodando na porta ${port}`);
});
