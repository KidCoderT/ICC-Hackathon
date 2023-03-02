import React from "react";
import * as Chakra from "@chakra-ui/react";
import { ChevronDownIcon, ViewIcon } from "@chakra-ui/icons";
import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";

let blocks = [
  {
    label: "AA",
    rows: [
      { name: "a", seats: [true, false] },
      { name: "b", seats: [true, true] },
      { name: "c", seats: [false, false] },
    ],
  },
  {
    label: "BB",
    rows: [
      { name: "a", seats: [true, false, false] },
      { name: "b", seats: [true, true, true] },
      { name: "c", seats: [false, false, true] },
      { name: "d", seats: [false, true, true] },
    ],
  },
];

const SelectSeat = () => {
  const { isOpen, onOpen, onClose } = Chakra.useDisclosure();

  const [block, setBlock] = React.useState("");
  const [blockIndex, setBlockIndex] = React.useState(-1);
  const [seatRowName, setSeatRowName] = React.useState("");
  const [seatRow, setSeatRow] = React.useState(-1);
  const [seatNo, setSeatNo] = React.useState(-1);

  const threeRef = useRef();
  const [camera, setCamera] = useState();
  const [renderer, setRenderer] = useState();
  const [controls, setControls] = useState();
  const [scene, setScene] = useState();
  const [model, setModel] = useState();

  React.useEffect(() => {
    console.log(seatRow, seatNo);
    if (threeRef.current) {
  //     // adding a new scene
  //     const newScene = new THREE.Scene();

      // adding a new camera
      const newCamera = new THREE.PerspectiveCamera(
        75,
        window.innerWidth / window.innerHeight,
        0.1,
        1000
      );
      newCamera.position.z = 5;

      // creating a new renderer
      const newRenderer = new THREE.WebGLRenderer();
      newRenderer.setSize(window.innerWidth, window.innerHeight);
      threeRef.current.appendChild(newRenderer.domElement);

  //     //new controls
  //     const newControls = new OrbitControls(newCamera, newRenderer.domElement);
  //     newControls.enableDamping = true;
  //     newControls.dampingFactor = 0.05;
  //     newControls.screenSpacePanning = false;
  //     newControls.minDistance = 1;
  //     newControls.maxDistance = 50;
  //     newControls.maxPolarAngle = Math.PI / 2;

  //     // loading the 3D model
  //     const loader = new THREE.GLTFLoader();
  //     loader.load("/path/to/your/3d-model.glb", (gltf) => {
  //       const newModel = gltf.scene;
  //       newScene.add(newModel);
  //       setModel(newModel);
  //     });

      setCamera(newCamera);
      setRenderer(newRenderer);
      setControls(newControls);
      setScene(newScene);
    
   }}, [block, blockIndex, seatRow, seatNo]);

  return (
    <>
      <Chakra.Modal onClose={onClose} size={"full"} isOpen={isOpen}>
        <Chakra.ModalOverlay />
        <Chakra.ModalContent>
          <Chakra.ModalHeader>Seat Viewing</Chakra.ModalHeader>
          <Chakra.ModalCloseButton />
          <Chakra.ModalBody background={"black"}>
            {/* Seat Viewing */}
            <canvas
            style={{ width: "100%", height: "100%" }}
            ref={threeRef}
          />
          {camera && (
            <Chakra.Script>
              {new Promise((resolve) => {
                const loader = new THREE.GLTFLoader();
                loader.load(
                  "icc-website/src/assets/3d-model.fbx",
                  (gltf) => {
                    const newModel = gltf.scene;
                    scene.add(newModel);
                    setModel(newModel);
                    resolve();
                  }
                );
              }).then(() => {
                const animate = () => {
                  requestAnimationFrame(animate);
                  controls.update();
                  renderer.render(scene, camera);
                };
                animate();
              })}
            </Chakra.Script>
          )}

          </Chakra.ModalBody>
          <Chakra.ModalFooter textAlign={"center"}>
            <Chakra.Heading size={"md"}>Block: AA, Seat: NAN</Chakra.Heading>
          </Chakra.ModalFooter>
        </Chakra.ModalContent>
      </Chakra.Modal>

      <Chakra.Flex
        alignItems={"center"}
        justifyContent="center"
        as="main"
        color="whiteAlpha.800"
        background="blackAlpha.900"
        minH={"100vh"}
      >
        <Chakra.Box
          minW="400px"
          maxW="600px"
          boxShadow="xs"
          bg="black"
          py={10}
          px={5}
          borderRadius="xl"
        >
          <Chakra.Heading size="lg" textAlign={"center"}>
            Chinna Swami Stadium
          </Chakra.Heading>
          <Chakra.Box
            borderRadius="full"
            h={1}
            w="100%"
            my={6}
            bg="whiteAlpha.700"
          />

          <Chakra.Flex
            w="100%"
            justifyContent={"space-evenly"}
            py={2}
            mb={6}
            borderRadius="lg"
            bg={"whiteAlpha.200"}
          >
            <Chakra.Heading size="sm">
              <span style={{ textTransform: "capitalize" }}>AUS</span>
            </Chakra.Heading>
            <Chakra.Text size="sm">vs</Chakra.Text>
            <Chakra.Heading size="sm">
              <span style={{ textTransform: "capitalize" }}>IND</span>
            </Chakra.Heading>
          </Chakra.Flex>

          <Chakra.Flex
            alignItems={"center"}
            justifyContent="space-between"
            my={3}
          >
            <Chakra.Heading size="md" mr={20}>
              Stadium Block:{" "}
            </Chakra.Heading>
            <Chakra.Menu>
              <Chakra.MenuButton
                flexGrow={1}
                as={Chakra.Button}
                rightIcon={<ChevronDownIcon />}
                colorScheme="whiteAlpha"
                variant="outline"
              >
                {block || "Choose..."}
              </Chakra.MenuButton>

              <Chakra.MenuList colorScheme="whiteAlpha" variant="outline">
                {blocks.map((item, key) => (
                  <Chakra.MenuItem
                    key={key}
                    color="black"
                    onClick={() => {
                      setBlock(item.label);
                      setBlockIndex(key);
                      setSeatRowName("");
                      setSeatRow(-1);
                      setSeatNo(-1);
                    }}
                  >
                    {item.label}
                  </Chakra.MenuItem>
                ))}
              </Chakra.MenuList>
            </Chakra.Menu>
          </Chakra.Flex>

          {block.length > 0 ? (
            <>
              <Chakra.Box
                borderRadius="full"
                h={0.5}
                w="100%"
                my={3}
                bg="whiteAlpha.700"
              />
              <Chakra.Flex
                alignItems={"center"}
                justifyContent="center"
                mb={3}
                flexDir="column"
              >
                <Chakra.Heading size="lg" mb={1}>
                  Seats
                </Chakra.Heading>
                <Chakra.Text size="sm" mb={2}>
                  Row Name: {seatRowName || "NA"}, Seat No:{" "}
                  {seatNo > 0 ? seatNo : "NA"}
                </Chakra.Text>

                {blocks[blockIndex].rows.map((row, row_idx) => (
                  <Chakra.Box key={row_idx}>
                    {row.seats.map((disabled, idx) => (
                      <Chakra.Button
                        w={4}
                        h={4}
                        m={2}
                        bg="red"
                        key={idx}
                        isDisabled={disabled}
                        onClick={() => {
                          setSeatRowName(row.name);
                          setSeatRow(row_idx);
                          setSeatNo(idx + 1);
                        }}
                        _hover={{
                          bg: !disabled ? "whiteAlpha.900" : "red",
                        }}
                        _active={{
                          bg: "blue",
                        }}
                        isActive={seatRowName === row.name && seatNo == idx + 1}
                      />
                    ))}
                  </Chakra.Box>
                ))}
              </Chakra.Flex>
              <Chakra.Box
                borderRadius="full"
                h={0.5}
                w="100%"
                my={3}
                bg="whiteAlpha.700"
              />
            </>
          ) : (
            <></>
          )}

          <Chakra.Button
            rightIcon={<ViewIcon />}
            colorScheme="blue"
            variant="outline"
            onClick={onOpen}
            w="100%"
          >
            View Stadium
          </Chakra.Button>
          <Chakra.Button
            colorScheme="green"
            // On click go to login
            w="100%"
            mt={2}
          >
            BOOK NOW
          </Chakra.Button>
        </Chakra.Box>
      </Chakra.Flex>
    </>
  );
};

export default SelectSeat;
