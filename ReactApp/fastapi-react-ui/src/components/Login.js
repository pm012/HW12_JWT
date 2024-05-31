import React from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Formik, Form, Field, ErrorMessage } from 'formik';
import { login } from '../../redux/authSlice';
import * as Yup from 'yup';

const Login = () => {
  const dispatch = useDispatch();
  const { error } = useSelector(state => state.auth);

  const initialValues = {
    username: '',
    password: '',
  };

  const validationSchema = Yup.object({
    username: Yup.string().required('Required'),
    password: Yup.string().required('Required'),
  });

  const onSubmit = (values) => {
    dispatch(login(values));
  };

  return (
    <div>
      <h1>Login</h1>
      <Formik initialValues={initialValues} validationSchema={validationSchema} onSubmit={onSubmit}>
        <Form>
          <div>
            <label>Username</label>
            <Field name="username" type="text" />
            <ErrorMessage name="username" component="div" />
          </div>
          <div>
            <label>Password</label>
            <Field name="password" type="password" />
            <ErrorMessage name="password" component="div" />
          </div>
          <button type="submit">Login</button>
          {error && <div>{error}</div>}
        </Form>
      </Formik>
    </div>
  );
};

export default Login;
