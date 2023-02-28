import React from "react";
import ReactDOM from "react-dom/client";
import { ChakraProvider, extendTheme } from '@chakra-ui/react'
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";
import Matches from "./pages/Matches";

const colors = {
  brand: {},
}

const router = createBrowserRouter([
  {
    path: "/",
    element: <Matches />,
  },
]);

const theme = extendTheme({ colors })

const rootElement = document.getElementById('root')
ReactDOM.createRoot(rootElement).render(
  <React.StrictMode>
    <ChakraProvider theme={theme}>
      <RouterProvider router={router} />
    </ChakraProvider>
  </React.StrictMode>,
)