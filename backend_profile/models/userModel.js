import mongoose from "mongoose";

const userSchema = mongoose.Schema(
    {
      email: {
        type: String,
        required: true,
        unique: true,
      },
      
      userName: {
        type: String,
        required: true,
      },
  
      password: {
        type: String,
        required: true,
        minLength: 6,
      },
  
    },
    { timestamps: true }
  );
  
  const UserModel = mongoose.model("User", userSchema);
  
  export default UserModel;