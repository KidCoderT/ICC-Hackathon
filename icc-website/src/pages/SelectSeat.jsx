import React from "react";
import * as Chakra from "@chakra-ui/react";
import { ChevronDownIcon, ViewIcon } from "@chakra-ui/icons";
import { useParams } from "react-router-dom";
import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";
import { Navigate } from "react-router-dom";

function easeOutCirc(x) {
  return Math.sqrt(1 - Math.pow(x - 1, 4));
}

const SelectSeat = () => {
  const { isOpen, onOpen, onClose } = Chakra.useDisclosure();
  const { matchId } = useParams();

  const [block, setBlock] = React.useState("");
  const [blockIndex, setBlockIndex] = React.useState(-1);
  const [seatRowName, setSeatRowName] = React.useState("");
  const [seatRow, setSeatRow] = React.useState(-1);
  const [seatNo, setSeatNo] = React.useState(-1);
  const [match, setMatch] = React.useState(null);
  const [valid, setValid] = React.useState(false);

  const [error, setError] = React.useState(false);

  const refContainer = React.useRef();
  const [loading, setLoading] = React.useState(true);
  const refRenderer = React.useRef();
  const urlDogGLB = "./../assets/3d-model.obj";

  const handleWindowResize = React.useCallback(() => {
    const { current: renderer } = refRenderer;
    const { current: container } = refContainer;
    if (container && renderer) {
      const scW = container.clientWidth;
      const scH = container.clientHeight;

      renderer.setSize(scW, scH);
    }
  }, []);

  /* eslint-disable react-hooks/exhaustive-deps */
  React.useEffect(() => {
    const { current: container } = refContainer;

    if (container) {
      const scW = container.clientWidth;
      const scH = container.clientHeight;

      const renderer = new THREE.WebGLRenderer({
        antialias: true,
        alpha: true,
      });

      renderer.setPixelRatio(window.devicePixelRatio);
      renderer.setSize(scW, scH);
      renderer.outputEncoding = THREE.sRGBEncoding;
      container.appendChild(renderer.domElement);
      refRenderer.current = renderer;
      const scene = new THREE.Scene();

      const target = new THREE.Vector3(-0.5, 1.2, 0);
      const initialCameraPosition = new THREE.Vector3(
        20 * Math.sin(0.2 * Math.PI),
        10,
        20 * Math.cos(0.2 * Math.PI)
      );

      // 640 -> 240
      // 8   -> 6
      const scale = scH * 0.005 + 4.8;
      const camera = new THREE.OrthographicCamera(
        -scale,
        scale,
        scale,
        -scale,
        0.01,
        50000
      );
      camera.position.copy(initialCameraPosition);
      camera.lookAt(target);

      const ambientLight = new THREE.AmbientLight(0xcccccc, 1);
      scene.add(ambientLight);

      const controls = new OrbitControls(camera, renderer.domElement);
      controls.autoRotate = true;
      controls.target = target;

      const geometry = new THREE.BoxGeometry( 1, 1, 1 );
      const material = new THREE.MeshBasicMaterial( { color: 0x00ff00 } );
      const cube = new THREE.Mesh( geometry, material );
      // const loader = new THREE.GLTFLoader();
      // loader.load(urlDogGLB, (obj) => {
      //   const newModel = obj.scene;
      //   scene.add(newModel);
      //   setModel(newModel);
      //   resolve();
      //   animate();
      // });

      let req = null;
      let frame = 0;

      const animate = () => {
        req = requestAnimationFrame(animate);

        // frame = frame <= 100 ? frame + 1 : frame

        // if (frame <= 100) {
        //   const p = initialCameraPosition
        //   const rotSpeed = -easeOutCirc(frame / 120) * Math.PI * 20

        //   camera.position.y = 10
        //   camera.position.x =
        //     p.x * Math.cos(rotSpeed) + p.z * Math.sin(rotSpeed)
        //     camera.position.z =
        //     p.z * Math.cos(rotSpeed) - p.x * Math.sin(rotSpeed)
        //     camera.lookAt(target)
        // } else {
        //   controls.update()
        // }

        renderer.render(scene, camera);
      };

      return () => {
        cancelAnimationFrame(req);
        renderer.domElement.remove();
        renderer.dispose();
      };
    }
  }, []);

  React.useEffect(() => {
    window.addEventListener("resize", handleWindowResize, false);
    return () => {
      window.removeEventListener("resize", handleWindowResize, false);
    };
  }, [handleWindowResize]);

  const validate = () => {
    if (block === "" || blockIndex === -1) {
      return setError("Block is Not Selected");
    }
    if (seatRowName === "" || seatRow === -1 || seatNo === -1) {
      return setError("Seat Is Not Selected");
    }

    setValid(true);
  };

  React.useEffect(() => {
    fetch(
      `https://localhost:8080/match/get/${matchId}`
    )
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        setMatch(data);
      })
      .catch((error) => {
        console.error(error);
      });
  }, []);

  // React.useState(() => {
  //   const newScene = new THREE.Scene();
  //   // adding a new camera
  //   const newCamera = new THREE.PerspectiveCamera(
  //     75,
  //     window.innerWidth / window.innerHeight,
  //     0.1,
  //     1000
  //   );
  //   newCamera.position.z = 5;

  //   // creating a new renderer
  //   // const newRenderer = new THREE.WebGLRenderer();
  //   // newRenderer.setSize(window.innerWidth, window.innerHeight);
  //   // threeRef.current.appendChild(newRenderer.domElement);

  //   // const newControls = new OrbitControls(newCamera, newRenderer.domElement);

  //   // setCamera(newCamera);
  //   // setRenderer(newRenderer);
  //   // setControls(newControls);
  //   // setScene(newScene);
  // }, []);

  return (
    <>
      <Chakra.Modal onClose={onClose} size={"full"} isOpen={isOpen}>
        <Chakra.ModalOverlay />
        <Chakra.ModalContent h="100vh">
          <Chakra.ModalHeader>Seat Viewing</Chakra.ModalHeader>
          <Chakra.ModalCloseButton />
          <Chakra.ModalBody background={"black"} style={{ display: "flex" }}>
            {/* Seat Viewing */}
            {/* <canvas style={{ width: "100%", height: "100%" }} ref={threeRef} />
            {camera && (
              <Chakra.Script>
                {new Promise((resolve) => {
                  const loader = new THREE.GLTFLoader();
                  loader.load("icc-website/src/assets/3d-model.fbx", (gltf) => {
                    const newModel = gltf.scene;
                    scene.add(newModel);
                    setModel(new THREE.Object3D().copy(newModel));
                    resolve();
                  });
                }).then(() => {
                  const animate = () => {
                    requestAnimationFrame(animate);
                    controls.update();
                    renderer.render(scene, camera);
                  };
                  animate();
                })}
              </Chakra.Script>
            )} */}
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
        {match !== null ? (
          <Chakra.Box
            minW="400px"
            maxW="600px"
            boxShadow="xs"
            bg="black"
            py={8}
            px={5}
            borderRadius="xl"
          >
            <Chakra.Heading
              size="lg"
              textAlign={"center"}
              textTransform="capitalize"
            >
              {match["stadium_name"]}
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
                <span style={{ textTransform: "capitalize" }}>
                  {match["country1"]}
                </span>
              </Chakra.Heading>
              <Chakra.Text size="sm">vs</Chakra.Text>
              <Chakra.Heading size="sm">
                <span style={{ textTransform: "capitalize" }}>
                  {match["country2"]}
                </span>
              </Chakra.Heading>
            </Chakra.Flex>

            <Chakra.Flex
              alignItems={"center"}
              justifyContent="space-between"
              my={3}
            >
              <Chakra.Heading size="md" mr={20}>
                Stadium Block:
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
                  {match["blocks"].map((item, key) => (
                    <Chakra.MenuItem
                      key={key}
                      color="black"
                      onClick={() => {
                        setBlock(item.name);
                        setBlockIndex(key);
                        setSeatRowName("");
                        setSeatRow(-1);
                        setSeatNo(-1);
                      }}
                    >
                      {item.name}
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

                  {match["blocks"][blockIndex].rows.map((row, row_idx) => (
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
                          isActive={
                            seatRowName === row.name && seatNo == idx + 1
                          }
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
              onClick={validate}
              w="100%"
              mt={2}
            >
              BOOK NOW
            </Chakra.Button>

            {error && (
              <Chakra.Alert
                mt={2}
                borderRadius="lg"
                status="error"
                variant="solid"
              >
                <Chakra.AlertIcon />
                <Chakra.AlertDescription>{error}</Chakra.AlertDescription>
              </Chakra.Alert>
            )}

            {valid && <Navigate to={`/book?info=${JSON.stringify({'match_id': match["id"], 'stadium_name': match["stadium_name"], 'block': block, 'seat_row': seatRow, 'seat_no': seatNo})}`} replace={true} />}
            
          </Chakra.Box>
        ) : (
          <></>
        )}
      </Chakra.Flex>
    </>
  );
};

export default SelectSeat;
