import React, { useEffect, useState } from 'react';
import { useSelector } from 'react-redux';
import axiosInstance from '../axiosConfig';


const Profile = () => {
  const { token } = useSelector(state => state.auth);
  const [profile, setProfile] = useState({});
  const [loading, setLoading] = useState(true);
  const [avatar, setAvatar] = useState(null);

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const response = await axiosInstance.get('/api/users/me', {
          headers: { Authorization: `Bearer ${token}` },
        });
        setProfile(response.data);
      } catch (error) {
        console.error(error);
      } finally {
        setLoading(false);
      }
    };
    fetchProfile();
  }, [token]);

  const handleAvatarChange = (e) => {
    setAvatar(e.target.files[0]);
  };

  const handleAvatarUpload = async () => {
    const formData = new FormData();
    formData.append('avatar', avatar);
    try {
      await axiosInstance.patch('/api/users/avatar', formData, {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'multipart/form-data',
        },
      });
    } catch (error) {
      console.error(error);
    }
  };

  if (loading) return <div>Loading...</div>;

  return (
    <div>
      <h1>Profile</h1>
      <div>
        <label>Username:</label>
        <span>{profile.username}</span>
      </div>
      <div>
        <label>Email:</label>
        <span>{profile.email}</span>
      </div>
      <div>
        <label>Avatar:</label>
        <input type="file" onChange={handleAvatarChange} />
        <button onClick={handleAvatarUpload}>Upload</button>
      </div>
    </div>
  );
};

export default Profile;
