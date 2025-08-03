import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import "@radix-ui/themes/styles.css";
import { Theme } from '@radix-ui/themes';

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);
root.render(
  <React.StrictMode>
    <Theme
      scaling="100%"
      radius="large"
      appearance="dark"
      panelBackground="solid"
      accentColor="mint"
      grayColor="gray"
    >
      <App />
    </Theme>
  </React.StrictMode>
);