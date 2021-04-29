import React from "react";
import { useHistory } from "react-router";
import { Container, Row, Col, Card } from "react-bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";
import { Paper, makeStyles, Grid } from "@material-ui/core";
import AppBar from "@material-ui/core/AppBar";
import Toolbar from "@material-ui/core/Toolbar";
import Typography from "@material-ui/core/Typography";
import Button from "@material-ui/core/Button";
import "./css/Home.css";
import sample from "./videos/background_video.mp4";

const Home = () => {
  const useStyles = makeStyles((theme) => ({
    root: {
      flexGrow: 1,
    },
    menuButton: {
      marginRight: theme.spacing(2),
    },
    title: {
      flexGrow: 1,
    },
    subtitle: {
      flexGrow: 2,
      color: "white",
      textAlign: "right",
    },
  }));

  const classes = useStyles();
  let history = useHistory();

  return (
    <>
      {/* <div className={classes.root}>
        <AppBar position="static">
          <Toolbar>
            <Typography variant="h6" className={classes.title}>
              Masl
            </Typography>
            <Typography className={classes.subtitle}>나를 위한 동네, 마이 슬세권</Typography>
          </Toolbar>
        </AppBar>
      </div>
          <Grid item xs={12} style={{ marginTop: '10rem'}}>
          <Row>
            <Col item xs={3}><div></div></Col>
            <Col item xs={6}>
          <Container>
            <Paper>
              <Button color="primary" size="large" onClick={(e)=>window.location.replace('/userinfo')}>마슬 찾아보기</Button>
            </Paper>
          </Container>
          </Col>
          <Col item xs={3}><div></div></Col>
          </Row>
          </Grid> */}

      <Grid item xs={12} style={{ backgroundColor: "#f8f8f8" }}>
        <Row style={{ margin: 0 }}>
          <div class="jb-box">
            <video autoPlay loop muted>
              <source src={sample} type="video/mp4" />
            </video>
          </div>
        </Row>
        <Row></Row>
      </Grid>
    </>
  );
};

export default Home;
