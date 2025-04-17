import express from "express";
import { Profile, signin, signup, deleteAccount } from "../controllers/userController.js";
import middleware from "../middleware.js";

const router = express.Router();

router.post("/signup", signup);
router.post("/signin", signin);
router.get("/profile", middleware, Profile);
router.delete('/delete', middleware, deleteAccount);

export default router;