import React, { useState, useEffect } from 'react';
import { useSelector } from 'react-redux';
import axiosInstance from '../axiosConfig';
import ContactForm from './ContactForm';

const Contacts = () => {
  const [contacts, setContacts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editContact, setEditContact] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const { token } = useSelector(state => state.auth);

  const fetchContacts = async () => {
    try {
      const response = await axiosInstance.get('/api/contacts', {
        headers: { Authorization: `Bearer ${token}` },
      });
      setContacts(response.data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async () => {
    try {
      const response = await axiosInstance.get(`/api/contacts/search?query=${searchQuery}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setContacts(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  const handleAddContact = async (values) => {
    try {
      await axiosInstance.post('/api/contacts', values, {
        headers: { Authorization: `Bearer ${token}` },
      });
      fetchContacts(); // Refresh the contacts list
    } catch (error) {
      console.error(error);
    }
  };

  const handleEditContact = async (contactId, values) => {
    try {
      await axiosInstance.patch(`/api/contacts/${contactId}`, values, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setEditContact(null);
      fetchContacts(); // Refresh the contacts list
    } catch (error) {
      console.error(error);
    }
  };

  const handleDeleteContact = async (contactId) => {
    try {
      await axiosInstance.delete(`/api/contacts/${contactId}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      fetchContacts(); // Refresh the contacts list
    } catch (error) {
      console.error(error);
    }
  };

  const handleFetchBirthdays = async () => {
    try {
      const response = await axiosInstance.get('/api/contacts/birthdays', {
        headers: { Authorization: `Bearer ${token}` },
      });
      setContacts(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    fetchContacts();
  }, [token]);

  if (loading) return <div>Loading...</div>;

  return (
    <div>
      <h1>Contacts</h1>
      <input
        type="text"
        placeholder="Search contacts"
        value={searchQuery}
        onChange={(e) => setSearchQuery(e.target.value)}
      />
      <button onClick={handleSearch}>Search</button>
      <button onClick={() => setShowForm(!showForm)}>Add Contact</button>
      <button onClick={handleFetchBirthdays}>Upcoming Birthdays</button>
      {showForm && (
        <ContactForm
          initialValues={{
            name: '',
            surname: '',
            email: '',
            phone: '',
            birth_date: '',
            additional_data: '',
          }}
          onSubmit={handleAddContact}
        />
      )}
      {editContact && (
        <ContactForm
          initialValues={editContact}
          onSubmit={(values) => handleEditContact(editContact.id, values)}
        />
      )}
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Surname</th>
            <th>Email</th>
            <th>Phone</th>
            <th>Birth Date</th>
            <th>Additional Data</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {contacts.map(contact => (
            <tr key={contact.id}>
              <td>{contact.name}</td>
              <td>{contact.surname}</td>
              <td>{contact.email}</td>
              <td>{contact.phone}</td>
              <td>{contact.birth_date}</td>
              <td>{contact.additional_data}</td>
              <td>
                <button onClick={() => setEditContact(contact)}>Edit</button>
                <button onClick={() => handleDeleteContact(contact.id)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Contacts;
