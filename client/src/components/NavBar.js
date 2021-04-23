import React from 'react';

import { makeStyles } from '@material-ui/core';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';

function NavBar() {
    const useStyles = makeStyles((theme) => ({
        root: {
          flexGrow: 1,
        },
        title: {
          flexGrow: 1,
        },
        subtitle: {
          flexGrow: 2,
          color: 'white',
          textAlign: 'right'
        }
    }));
    const classes = useStyles();

  return (
    <div className={classes.root}>
      <AppBar position="static">
            <Toolbar>
              <Typography variant="h6" className={classes.title}>
                Masl
              </Typography>
              <Typography className={classes.subtitle}>나를 위한 동네, 마이 슬세권</Typography>
            </Toolbar>
        </AppBar>
    </div>
  );
}

export default NavBar;