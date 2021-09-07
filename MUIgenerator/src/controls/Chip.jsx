import React from 'react';
import Avatar from '@material-ui/core/Avatar';
import Chip from '@material-ui/core/Chip';
import FaceIcon from '@material-ui/icons/Face';
import DoneIcon from '@material-ui/icons/Done';

export const JDIchips = ({ group }) => {

    const handleDelete = () => {
        console.info('You clicked the delete icon.');
    };

    const handleClick = () => {
        console.info('You clicked the Chip.');
    };

    const renderChip = (item) => {
        const basicChips = [
            <Chip data-label="chip" key={item.label}  label="Basic" {...item} />,
            <Chip data-label="chip" key={item.label}  label="Disabled" disabled {...item} />,
            <Chip data-label="chip" key={item.label}  avatar={<Avatar>M</Avatar>} label="Clickable" onClick={handleClick} {...item} />,
            <Chip data-label="chip" key={item.label} 
                avatar={<Avatar alt="Natacha" src="/static/images/avatar/1.jpg" />}
                label="Deletable"
                onDelete={handleDelete}
                {...item}
            />,
            <Chip data-label="chip" key={item.label} 
                icon={<FaceIcon data-label="icon" />}
                label="Clickable deletable"
                onClick={handleClick}
                onDelete={handleDelete}
                {...item}
            />,
            <Chip data-label="chip" key={item.label} 
                label="Custom delete icon"
                onClick={handleClick}
                onDelete={handleDelete}
                deleteIcon={<DoneIcon data-label="icon" />}
                {...item}
            />,
            <Chip data-label="chip" key={item.label}  label="Clickable Link" component="a" href="#chip" clickable {...item} />,
            <Chip data-label="chip" key={item.label} 
                avatar={<Avatar>M</Avatar>}
                label="Primary clickable"
                clickable
                color="primary"
                onDelete={handleDelete}
                deleteIcon={<DoneIcon data-label="icon" />}
                {...item}
            />,
            <Chip data-label="chip" key={item.label} 
                icon={<FaceIcon data-label="icon" />}
                label="Primary clickable"
                clickable
                color="primary"
                onDelete={handleDelete}
                deleteIcon={<DoneIcon data-label="icon" />}
                {...item}
            />,
            <Chip data-label="chip" key={item.label}  label="Deletable primary" onDelete={handleDelete} color="primary" {...item} />,
            <Chip data-label="chip" key={item.label} 
                icon={<FaceIcon data-label="icon" />}
                label="Deletable secondary"
                onDelete={handleDelete}
                color="secondary"
                {...item}
            />,
        ];
        return basicChips[item.typenumber];
    };

    const renderGroup = () => {
        const chipsGroup = [];
        group.forEach((item) => {
            chipsGroup.push(renderChip(item));
        })
        return chipsGroup;
    }

    return renderGroup();
}
