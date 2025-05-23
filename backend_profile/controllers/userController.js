import bcrypt from "bcryptjs";
import jwt from "jsonwebtoken";
import UserModel from "../models/userModel.js";

export const signup = async (req, res) => {
    const { email, userName, password } = req.body;
  
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    console.log("Signup request received", req.body);
    try {
      
      if (!emailRegex.test(email)) {
        return res.status(400).json({ message: "Invalid email format" });
      }
  
      const existingUser = await UserModel.findOne({ email });
      if (existingUser)
        return res.status(400).json({ message: "User already exists" });
  
      const hashedPassword = await bcrypt.hash(password, 10);
  
      const user = await UserModel.create({
        email,
        userName,
        password: hashedPassword,
      });
  
      res.status(201).json({ message: "User registered successfully" });
    } catch (error) {
      res.status(500).json({ message: "Server error", error });
    }
  };

  export const signin = async (req, res) => {
    const { email, password } = req.body;
  
    try {
      const user = await UserModel.findOne({ email });
      if (!user) return res.status(400).json({ message: "User not found" });
  
      const isMatch = await bcrypt.compare(password, user.password);
      if (!isMatch)
        return res.status(400).json({ message: "Invalid credentials" });
  
      const token = jwt.sign({ id: user._id }, process.env.JWT_SECRET, {
        expiresIn: "1h",
      });

      return res.status(200).json({
        message: "User logged in successfully",
        token,
        user: { id: user._id, userName: user.userName, email: user.email },
      });
    } catch (error) {
      res.status(500).json({ message: "Server error", error });
    }
  };

  export const Profile = async (req, res) => {
    try {
      const user = await UserModel.findById(req.user.id).select("-password");
      if (!user) return res.status(404).json({ message: "User not found" });
  
      res.status(200).json(user);
    } catch (error) {
      res.status(500).json({ message: "Server error", error });
    }
  };

  export const deleteAccount = async (req, res) => {
    try {
        console.log("Request received for user deletion:", req.user);
  
        
        if (!req.user || !req.user.id) {
            console.error("User ID not found in request");
            return res.status(400).json({ message: "User ID missing in request" });
        }
  
        const userId = req.user.id;
        console.log("Attempting to delete user with ID:", userId);
  
        const deletedUser = await UserModel.findByIdAndDelete(userId);
  
        if (!deletedUser) {
            console.error("User not found for deletion:", userId);
            return res.status(404).json({ message: "User not found" });
        }
  
        console.log("User deleted successfully:", deletedUser);
        res.json({ message: "Account deleted successfully" });
    } catch (error) {
        console.error("Error in deleteAccount function:", error);
        res.status(500).json({ message: "Error deleting account", error: error.message });
    }
  };
  