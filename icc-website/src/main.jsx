import React from "react";
import ReactDOM from "react-dom/client";
import { ChakraProvider, extendTheme } from "@chakra-ui/react";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import Matches from "./pages/Matches";
import SelectSeat from "./pages/SelectSeat";
import BookTicket from "./pages/BookTicket";

const colors = {
  brand: {},
};

const router = createBrowserRouter([
  {
    path: "/",
    element: <Matches />,
  },
  {
    path: "seat/:matchId",
    element: <SelectSeat />,
  },
  {
    path: "book",
    element: <BookTicket />,
  },
]);

const theme = extendTheme({ colors });

const rootElement = document.getElementById("root");
ReactDOM.createRoot(rootElement).render(
  <React.StrictMode>
    <ChakraProvider theme={theme}>
      <RouterProvider router={router} />
    </ChakraProvider>
  </React.StrictMode>
);
