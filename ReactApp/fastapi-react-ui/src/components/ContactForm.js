import React from 'react';
import { Formik, Form, Field, ErrorMessage } from 'formik';
import * as Yup from 'yup';

const ContactForm = ({ initialValues, onSubmit }) => {
  const validationSchema = Yup.object({
    name: Yup.string().required('Required'),
    surname: Yup.string().required('Required'),
    email: Yup.string().email('Invalid email format').required('Required'),
    phone: Yup.string().required('Required'),
    birth_date: Yup.date().required('Required'),
    additional_data: Yup.string(),
  });

  return (
    <Formik initialValues={initialValues} validationSchema={validationSchema} onSubmit={onSubmit}>
      <Form>
        <div>
          <label>Name</label>
          <Field name="name" type="text" />
          <ErrorMessage name="name" component="div" />
        </div>
        <div>
          <label>Surname</label>
          <Field name="surname" type="text" />
          <ErrorMessage name="surname" component="div" />
        </div>
        <div>
          <label>Email</label>
          <Field name="email" type="email" />
          <ErrorMessage name="email" component="div" />
        </div>
        <div>
          <label>Phone</label>
          <Field name="phone" type="text" />
          <ErrorMessage name="phone" component="div" />
        </div>
        <div>
          <label>Birth Date</label>
          <Field name="birth_date" type="date" />
          <ErrorMessage name="birth_date" component="div" />
        </div>
        <div>
          <label>Additional Data</label>
          <Field name="additional_data" type="text" />
          <ErrorMessage name="additional_data" component="div" />
        </div>
        <button type="submit">Submit</button>
      </Form>
    </Formik>
  );
};

export default ContactForm;
