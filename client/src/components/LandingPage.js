import React from 'react';
import { useHistory } from 'react-router';

import { Container, Row, Col } from 'react-bootstrap';

import { Paper, makeStyles, Grid } from '@material-ui/core';
import Button from '@material-ui/core/Button';
import NavBar from './NavBar.js';


function Index() {
    const useStyles = makeStyles((theme) => ({
      menuButton: {
        marginRight: theme.spacing(2),
      }
    }));
    const classes = useStyles();
    const history = useHistory
    return (
      <div>
        <NavBar />
        <Grid item xs={12} style={{ marginTop: '10rem'}}>
        <Row>
            <Col item xs={3}><div></div></Col>
            <Col item xs={6}>
        <Container>
            <Row>
            <Col item xs={6}>
                <Paper>
                    <Button color="primary" size="large" onClick={(e)=>window.location.replace('/flowchart')}>나에게 알맞은 정보 찾기</Button>
                </Paper>
            </Col>
            <Col item xs={6}>
                <Paper>
                    <Button color="primary" size="large" onClick={(e)=>window.location.replace('/userinfo')}>마슬 찾아보기</Button>
                </Paper>
            </Col>
            </Row>
        </Container>
        </Col>
        <Col item xs={3}><div></div></Col>
        </Row>
        </Grid>
      </div>
    )
  }

export default Index;