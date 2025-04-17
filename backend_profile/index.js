import express from "express";
import dotenv from "dotenv";
import cors from "cors";
import userRoutes from "./routes/userRoutes.js";
import connectDb from "./db.js";

dotenv.config();
const PORT = process.env.PORT;
const app = express();

app.use(express.json());
app.use(cors());
connectDb();

app.use("/api/auth", userRoutes
);

app.listen(PORT, () => {
    console.log(`program listening ${PORT}`);
  });